import re

def clean_text(text: str) -> str:
    # Remove special chars, multiple spaces, bullet symbols
    text = re.sub(r"[\u2022•■-]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

