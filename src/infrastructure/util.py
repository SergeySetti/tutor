def clean_markdown(text: str) -> str:
    text = text.replace("**", "")

    # Strip leading and trailing whitespace
    text = text.strip()

    return text
