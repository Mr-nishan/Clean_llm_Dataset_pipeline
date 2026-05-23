import re

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()


def remove_duplicates(df):
    return df.drop_duplicates(subset=["text"]).reset_index(drop=True)


def remove_empty(df):
    text = df["text"]
    mask = text.notna() & (text.astype(str).str.strip() != "")
    return df[mask].reset_index(drop=True)
