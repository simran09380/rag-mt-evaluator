from pathlib import Path
import pandas as pd
import json


def read_csv(file_path: str | Path, encoding: str = "utf-8") -> list[dict]:
    """
    Read CSV dataset.
    """
    df = pd.read_csv(file_path, encoding=encoding)
    return df.to_dict(orient="records")


def read_txt(file_path: str | Path, encoding: str = "utf-8") -> list[dict]:
    """
    Read TXT dataset.

    Expected format:
    source ||| hypothesis ||| reference
    """

    records = []

    with open(file_path, "r", encoding=encoding) as file:
        for index, line in enumerate(file, start=1):

            line = line.strip()

            if not line:
                continue

            parts = [part.strip() for part in line.split("|||")]

            if len(parts) != 3:
                raise ValueError(
                    f"Invalid format at line {index}. "
                    "Expected: source ||| hypothesis ||| reference"
                )

            records.append({
                "id": index,
                "source": parts[0],
                "hypothesis": parts[1],
                "reference": parts[2]
            })

    return records

def read_jsonl(file_path: str | Path, encoding: str = "utf-8") -> list[dict]:
    """
    Read JSONL dataset.

    Returns:
        List of dictionaries.
    """

    records = []

    with open(file_path, "r", encoding=encoding) as file:
        for line in file:

            line = line.strip()

            if not line:
                continue

            records.append(json.loads(line))

    return records

def read_dataset(file_path, extension, encoding):
    if extension == ".csv":
        return read_csv(file_path, encoding)

    elif extension == ".txt":
        return read_txt(file_path, encoding)

    elif extension == ".jsonl":
        return read_jsonl(file_path, encoding)

    else:
        raise ValueError(f"Unsupported file format: {extension}")