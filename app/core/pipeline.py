# core/pipeline.py

import pandas as pd

from app.cleaner import clean_text, remove_duplicates, remove_empty
from app.tokenizer import tokenize_text
from app.annotator import create_prompt_response


def run_pipeline(df):
    # 🔒 Safety check: ensure DataFrame
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    df = df.copy()

    # normalize column names
    df.columns = df.columns.str.lower()

    # 🔒 Ensure required column exists
    if "text" not in df.columns:
        raise ValueError("Input data must contain a 'text' column")

    # cleaning steps (must return DataFrame)
    df = remove_empty(df)
    df = remove_duplicates(df)

    # text processing
    df["cleaned"] = df["text"].astype(str).apply(clean_text)
    df["tokens"] = df["cleaned"].apply(tokenize_text)

    # dataset creation (API/export format)
    dataset = []

    for text in df["cleaned"]:
        if text and str(text).strip():
            pair = create_prompt_response(text)
            if pair:
                dataset.append(pair)

    return df, dataset