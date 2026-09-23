from app.metrics.metric_engine import calculate_all_metrics
from app.ingestion.pipeline import ingest_dataset
from pipeline.preprocessing_pipeline import preprocess
from app.chunking.pipeline import build_chunks
from app.ingestion.validator import detect_dataset_type
from app.embeddings.embeddings import embed_chunks
from app.indexing.index_manager import IndexManager
from app.indexing.index_builder import build_indexes
from app.query_generation.pipeline import generate_queries
from app.retrieval.query_retrieval_service import QueryRetrievalService
from app.services.llm_evaluator import LLMEvaluator
from app.services.mqm_service import MQMService
from app.fusion.score_fusion import ScoreFusion

import uuid

index_manager = IndexManager()

def build_llm_evidence(retrieval_results, max_items=15):

    evidence = []
    seen = set()

    if not isinstance(retrieval_results, dict):
        return evidence

    for query_type, query_data in retrieval_results.items():

        if not isinstance(query_data, dict):
            continue

        results = query_data.get("results", [])

        if not isinstance(results, list):
            continue

        for result in results:

            if not isinstance(result, dict):
                continue

            source_text = result.get("source")

            translation_text = (
                result.get("target_text")
                or result.get("target")
            )

            if not translation_text:
                translation_text = None

            evidence_type = (
                result.get("chunk_type")
                or query_type
                or "retrieved"
            )

            relevance = result.get("relevance")

            chunk_id = result.get("chunk_id")

            dedupe_key = (
                chunk_id,
                source_text,
                translation_text,
                evidence_type
            )

            if dedupe_key in seen:
                continue

            seen.add(dedupe_key)

            evidence.append({
                "id": f"E{len(evidence) + 1}",
                "chunk_id": chunk_id,
                "source": source_text,
                "translation": translation_text,
                "type": evidence_type,
                 # Module 6 reranking information
                "relevance": relevance,
                "semantic_score": result.get("semantic_score"),
                "source_similarity": result.get("source_similarity"),
                "hypothesis_similarity": result.get("hypothesis_similarity"),
                "language_pair_score": result.get("language_pair_score"),
                "terminology_score": result.get("terminology_score"),
                "entity_score": result.get("entity_score"),
                "authority_score": result.get("authority_score"),
                "verification_score": result.get("verification_score"),
            })

            if len(evidence) >= max_items:
                return evidence

    return evidence

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

                # -------------------------
                # MODULE 7: METRICS
                # -------------------------
                metric_results = calculate_all_metrics(
                    source=record["source"],
                    hypothesis=record["hypothesis"],
                    reference=record.get("reference")
                )

                record["metrics"] = metric_results

                

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

            llm_evaluator = LLMEvaluator()
            mqm_service = MQMService()
            score_fusion = ScoreFusion()

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
                # -------------------------
                # MODULE 8: LLM EVALUATION
                # -------------------------

                evidence_items = build_llm_evidence(
                    record_retrieval
                )

                llm_evaluation = llm_evaluator.evaluate(
                    source=record["source"],
                    translation=record["hypothesis"],
                    source_lang=record.get("source_lang"),
                    target_lang=record.get("target_lang"),
                    domain=record.get("domain"),
                    reference=record.get("reference"),
                    evidence=evidence_items,
                    metrics=record.get("metrics"),
                    evaluation_instructions=None
                )

                mqm_service = MQMService()

                mqm_evaluation = mqm_service.classify(
                    source=record["source"],
                    translation=record["hypothesis"],
                    source_lang=record.get("source_lang"),
                    target_lang=record.get("target_lang"),
                    domain=record.get("domain"),
                    reference=record.get("reference"),
                    evidence=evidence_items,
                    llm_evaluation=llm_evaluation,
                )

                # ==================================================
                # MODULE 10: SCORE FUSION
                # ==================================================

                score_fusion = ScoreFusion()

                final_evaluation = score_fusion.calculate_score(
                    metrics=metric_results,
                    llm_evaluation=llm_evaluation,
                    mqm_evaluation=mqm_evaluation,
                    evidence=evidence_items,
                )

                record["llm_evaluation"] = llm_evaluation
                record["mqm_evaluation"] = mqm_evaluation
                record["final_evaluation"] = final_evaluation

                
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

    # ==================================================
    # MODULE 7: METRICS
    # ==================================================

    metric_results = calculate_all_metrics(
        source=source,
        hypothesis=hypothesis,
        reference=reference
    )

    
    
    # ==================================================
    # MODULE 8: EVIDENCE-GROUNDED LLM EVALUATION
    # ==================================================
    # Convert retrieval results into clean evidence
    
    evidence_items = build_llm_evidence(
        retrieval_results
    )


    llm_evaluator = LLMEvaluator()

    llm_evaluation = llm_evaluator.evaluate(
        source=source,
        translation=hypothesis,
        source_lang=source_lang,
        target_lang=target_lang,
        domain=domain,
        reference=reference,
        evidence=evidence_items,
        metrics=metric_results,
        evaluation_instructions=None
    )

    mqm_service = MQMService()

    mqm_evaluation = mqm_service.classify(
        source=source,
        translation=hypothesis,
        source_lang=source_lang,
        target_lang=target_lang,
        domain=domain,
        reference=reference,
        evidence=evidence_items,
        llm_evaluation=llm_evaluation,
    )

    # ==================================================
    # MODULE 10: SCORE FUSION
    # ==================================================

    score_fusion = ScoreFusion()

    final_evaluation = score_fusion.calculate_score(
        metrics=metric_results,
        llm_evaluation=llm_evaluation,
        mqm_evaluation=mqm_evaluation,
        evidence=evidence_items,
    )

    return {
        "source": source,
        "hypothesis": hypothesis,
        "reference": reference,
        "preprocessing": preprocessing_result,
        "chunks": chunk_result,
        "queries": generated_queries,
        "retrieval": retrieval_results,
        "metrics": metric_results,
        "llm_evaluation": llm_evaluation,
        "mqm_evaluation": mqm_evaluation,
        "final_evaluation": final_evaluation
    }


