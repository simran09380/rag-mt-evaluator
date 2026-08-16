from app.ingestion.pipeline import ingest_dataset
from pipeline.preprocessing_pipeline import preprocess
from app.chunking.pipeline import build_chunks


async def evaluate(
    file,
    source,
    hypothesis,
    reference,
    source_lang,
    target_lang,
    domain,
):

    # -------------------------
    # FILE INPUT
    # -------------------------
    if file:

        dataset = ingest_dataset(file)

        processed_records = []
        term_records = []
        entity_records = []
        for record in dataset["data"]:

            preprocessing_result = preprocess(
                record["source"],
                record["hypothesis"]
            )

            record["preprocessing"] = preprocessing_result

            processed_records.append(record)

            # -------------------------
        # MODULE 2 → MODULE 4
        # TERMINOLOGY
        # -------------------------

        source_language = preprocessing_result["source_language"]
        target_language = preprocessing_result["target_language"]

        # Source terminology
        for term in preprocessing_result["source_terminology"]:

            term_records.append({
                "term": term["term"],
                "language": source_language,
                "domain": record["domain"],
                "source_type": "extracted_terminology",
                "authority": "unknown"
            })

        # Target terminology
        for term in preprocessing_result["target_terminology"]:

            term_records.append({
                "term": term["term"],
                "language": target_language,
                "domain": record["domain"],
                "source_type": "extracted_terminology",
                "authority": "unknown"
            })

        # -------------------------
        # MODULE 2 → MODULE 4
        # NAMED ENTITIES
        # -------------------------

        for sentence_entities in preprocessing_result["source_entities"]:

            for entity in sentence_entities:

                entity_records.append({
                    "entity": entity["entity"],
                    "label": entity["label"],
                    "language": preprocessing_result["source_language"],
                    "domain": record["domain"],
                    "source_type": "named_entity_extraction",
                    "authority": "unknown"
                })


        for sentence_entities in preprocessing_result["target_entities"]:

            for entity in sentence_entities:

                entity_records.append({
                    "entity": entity["entity"],
                    "label": entity["label"],
                    "language": preprocessing_result["target_language"],
                    "domain": record["domain"],
                    "source_type": "named_entity_extraction",
                    "authority": "unknown"
                })
            dataset["data"] = processed_records

            # -------------------------
            # MODULE 4: CHUNKING
            # -------------------------
            chunk_result = build_chunks(
                sentence_records=dataset["data"],
                term_records=term_records,
                entity_records=entity_records
            )

        dataset["chunks"] = chunk_result

        return dataset

    # -------------------------
    # SINGLE SENTENCE
    # -------------------------
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
    return {
        "source": source,
        "hypothesis": hypothesis,
        "reference": reference,
        "preprocessing": preprocessing_result,
        "chunks": chunk_result
    }