def assign_sentence_ids(records: list[dict]) -> list[dict]:
    """
    Ensure every record has a unique sentence ID.

    If an ID already exists, keep it.
    Otherwise generate one.
    """
    updated_records=[]
    for index, record in enumerate(records, start=1):

        new_record = record.copy()

        if "id" not in new_record or str(new_record["id"]).strip() == "":
            new_record["id"] = f"sent_{index:06d}"

        updated_records.append(new_record)

    return updated_records