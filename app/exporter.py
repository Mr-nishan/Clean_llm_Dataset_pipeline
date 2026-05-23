import json
import os

def export_jsonl(data, path):
    """
    Save dataset as JSONL format (one JSON per line)
    """

    directory = os.path.dirname(path)

    # only create folder if path contains directory
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    return path