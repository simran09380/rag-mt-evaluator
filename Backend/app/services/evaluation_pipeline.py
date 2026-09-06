from app.ingestion.pipeline import ingest_dataset
from pipeline.preprocessing_pipeline import preprocess
from app.chunking.pipeline import build_chunks
from app.ingestion.validator import detect_dataset_type
from app.embeddings.embeddings import embed_chunks
from app.indexing.index_manager import IndexManager
from app.indexing.index_builder import build_indexes
from app.query_generation.pipeline import generate_queries
from app.retrieval.query_retrieval_service import QueryRetrievalService

import uuid

index_manager = IndexManager()

async def evaluate(
    file,
    source,
    hypothesis,
    reference,
    source_lang,
    target_lang,
    domain,
):

    # ==================================================
    # FILE INPUT
    # ==================================================
    if file:

        # -------------------------
        # MODULE 1: INGESTION
        # -------------------------
        dataset = ingest_dataset(file)

        dataset_type = detect_dataset_type(
            dataset["data"]
        )

        # ==================================================
        # TRANSLATION DATASET
        # ==================================================
        if dataset_type == "translation":

            processed_records = []
            term_records = []
            entity_records = []

            for record in dataset["data"]:

                # -------------------------
                # MODULE 2: PREPROCESSING
                # -------------------------
                preprocessing_result = preprocess(
                    record["source"],
                    record["hypothesis"]
                )

                record["preprocessing"] = preprocessing_result

                processed_records.append(record)

                # -------------------------
                # TERMINOLOGY
                # -------------------------
                source_language = (
                    preprocessing_result["source_language"]
                )

                target_language = (
                    preprocessing_result["target_language"]
                )

                for term in preprocessing_result[
                    "source_terminology"
                ]:

                    term_records.append({
                        "term": term["term"],
                        "language": source_language,
                        "domain": record["domain"],
                        "source_type": "extracted_terminology",
                        "authority": "unknown",
                        "document_id": record.get("document_id"),
                    })

                for term in preprocessing_result[
                    "target_terminology"
                ]:

                    term_records.append({
                        "term": term["term"],
                        "language": target_language,
                        "domain": record["domain"],
                        "source_type": "extracted_terminology",
                        "authority": "unknown",
                        "document_id": record.get("document_id"),
                    })

                # -------------------------
                # NAMED ENTITIES
                # -------------------------
                for sentence_entities in preprocessing_result[
                    "source_entities"
                ]:

                    for entity in sentence_entities:

                        entity_records.append({
                            "entity": entity["entity"],
                            "label": entity["label"],
                            "language": source_language,
                            "domain": record["domain"],
                            "source_type": (
                                "named_entity_extraction"
                            ),
                            "authority": "unknown",
                            "document_id": record.get("document_id"),
                        })

                for sentence_entities in preprocessing_result[
                    "target_entities"
                ]:

                    for entity in sentence_entities:

                        entity_records.append({
                            "entity": entity["entity"],
                            "label": entity["label"],
                            "language": target_language,
                            "domain": record["domain"],
                            "source_type": (
                                "named_entity_extraction"
                            ),
                            "authority": "unknown",
                            "document_id": record.get("document_id"),
                        })

            # -------------------------
            # UPDATE DATA
            # -------------------------
            dataset["data"] = processed_records

            # -------------------------
            # MODULE 4: CHUNKING
            # -------------------------
            chunk_result = build_chunks(
                sentence_records=dataset["data"],
                term_records=term_records,
                entity_records=entity_records
            )

            embedded_chunks = embed_chunks(
                chunk_result["valid_chunks"]
            )

            chunk_result["valid_chunks"] = embedded_chunks

            build_indexes(
                embedded_chunks,
                index_manager
            )

            # ==================================================
            # MODULE 3 + MODULE 5
            # ==================================================

            query_results = []

            for record in dataset["data"]:

                record_queries = generate_queries(
                    source_text=record["source"],
                    mt_output=record["hypothesis"],
                    source_lang=record.get("source_lang"),
                    target_lang=record.get("target_lang"),
                    domain=record.get("domain")
                )

                query_retrieval_service = QueryRetrievalService(
                    chunks=embedded_chunks,
                    index_manager=index_manager
                )

                record_retrieval = (
                    query_retrieval_service.retrieve_generated_queries(
                        generated_queries=record_queries,
                        source_text=record["source"],
                        mt_output=record["hypothesis"],
                        query_metadata={
                            "language": record.get("source_lang"),
                            "domain": record.get("domain")
                        },
                        index_type="source",
                        top_k=5
                    )
                )

                query_results.append({
                    "record_id": record.get("id"),
                    "queries": record_queries,
                    "retrieval": record_retrieval
                })
            dataset["chunks"] = chunk_result
            dataset["query_retrieval"] = query_results

            return dataset

    
        # ==================================================
        # PARAGRAPH / DOMAIN DOCUMENT
        # ==================================================
        elif dataset_type == "paragraph":

            paragraph_records = []

            for record in dataset["data"]:

                paragraph_records.append({
                    "text": record["text"],
                    "language": record["language"],
                    "domain": record["domain"],
                    "source_type": record["source_type"],
                    "authority": record["authority"],
                    "document_id": record["document_id"],
                    "paragraph_id": record["paragraph_id"]
                })

            # -------------------------
            # MODULE 4: PARAGRAPH CHUNKING
            # -------------------------
            chunk_result = build_chunks(
                paragraph_records=paragraph_records
            )

            embedded_chunks = embed_chunks(
                chunk_result["valid_chunks"]
            )

            chunk_result["valid_chunks"] = embedded_chunks

            build_indexes(
                embedded_chunks,
                index_manager
            )

            
            dataset["chunks"] = chunk_result
            

            return dataset

        elif dataset_type == "section":

            section_records = []

            for record in dataset["data"]:

                section_records.append({
                    "text": record["text"],
                    "language": record["language"],
                    "domain": record["domain"],
                    "source_type": record["source_type"],
                    "authority": record["authority"],
                    "document_id": record["document_id"],
                    "section_id": record["section_id"],
                    "section_title": record["section_title"]
                })

            chunk_result = build_chunks(
                section_records=section_records
            )

            embedded_chunks = embed_chunks(
                chunk_result["valid_chunks"]
            )

            chunk_result["valid_chunks"] = embedded_chunks

            build_indexes(
                embedded_chunks,
                index_manager
            )

            

            dataset["chunks"] = chunk_result
            

            return dataset

    # ==================================================
    # SINGLE SENTENCE INPUT
    # ==================================================

    preprocessing_result = preprocess(
        source,
        hypothesis
    )

    sentence_record = {
        "id": 1,
        "source": source,
        "hypothesis": hypothesis,
        "reference": reference,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "domain": domain,
        "document_id": str(uuid.uuid4()),
    }

    chunk_result = build_chunks(
        sentence_records=[sentence_record]
    )

    embedded_chunks = embed_chunks(
        chunk_result["valid_chunks"]
    )

    chunk_result["valid_chunks"] = embedded_chunks

    build_indexes(
            embedded_chunks,
            index_manager
        )

    # ==================================================
    # MODULE 3: QUERY GENERATION
    # ==================================================

    generated_queries = generate_queries(
        source_text=source,
        mt_output=hypothesis,
        source_lang=source_lang,
        target_lang=target_lang,
        domain=domain
    )

    # ==================================================
    # MODULE 5: HYBRID RETRIEVAL
    # ==================================================

    query_retrieval_service = QueryRetrievalService(
        chunks=embedded_chunks,
        index_manager=index_manager
    )

    retrieval_results = (
        query_retrieval_service.retrieve_generated_queries(
            generated_queries=generated_queries,
            source_text=source,
            mt_output=hypothesis,
            query_metadata={
                "language": source_lang,
                "domain": domain
            },
            index_type="source",
            top_k=5
        )
    )

    

    return {
        "source": source,
        "hypothesis": hypothesis,
        "reference": reference,
        "preprocessing": preprocessing_result,
        "chunks": chunk_result,
        "queries": generated_queries,
        "retrieval": retrieval_results
    }

def build_indexes(
    embedded_chunks: list[dict],
    index_manager
):
    """
    Build and update all indexes using IndexManager.
    """

    return index_manager.build_all(
        embedded_chunks
    )