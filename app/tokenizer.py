def tokenize_text(text):
    if not text:
        return []
    return str(text).lower().split()