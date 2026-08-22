from app.ingestion.pipeline import ingest_dataset
from pipeline.preprocessing_pipeline import preprocess
from app.chunking.pipeline import build_chunks
from app.ingestion.validator import detect_dataset_type
from app.embeddings.embeddings import embed_chunks


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
                        "authority": "unknown"
                    })

                for term in preprocessing_result[
                    "target_terminology"
                ]:

                    term_records.append({
                        "term": term["term"],
                        "language": target_language,
                        "domain": record["domain"],
                        "source_type": "extracted_terminology",
                        "authority": "unknown"
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
                            "authority": "unknown"
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
                            "authority": "unknown"
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

            embedded_chunks = embed_chunks(chunk_result)

            dataset["chunks"] = embedded_chunks

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

            embedded_chunks = embed_chunks(chunk_result)

            dataset["chunks"] = embedded_chunks

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

            # EMBEDDINGS
            embedded_chunks = embed_chunks(chunk_result)

            dataset["chunks"] = embedded_chunks

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
    }

    chunk_result = build_chunks(
        sentence_records=[sentence_record]
    )

    # EMBEDDINGS
    embedded_chunks = embed_chunks(chunk_result)

    return {
        "source": source,
        "hypothesis": hypothesis,
        "reference": reference,
        "preprocessing": preprocessing_result,
        "chunks": embedded_chunks
    }