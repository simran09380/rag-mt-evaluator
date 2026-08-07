from app.ingestion.pipeline import ingest_dataset
from pipeline.preprocessing_pipeline import preprocess


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

        for record in dataset["data"]:

            preprocessing_result = preprocess(
                record["source"],
                record["hypothesis"]
            )

            record["preprocessing"] = preprocessing_result

            processed_records.append(record)

        dataset["data"] = processed_records

        return dataset

    # -------------------------
    # SINGLE SENTENCE
    # -------------------------
    preprocessing_result = preprocess(
        source,
        hypothesis
    )

    return {
        "source": source,
        "hypothesis": hypothesis,
        "reference": reference,
        "preprocessing": preprocessing_result
    }