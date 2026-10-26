
import re


def clean_text(text):
    """
    Normalize extracted resume text while preserving
    important technical terms such as C++, C#, and .NET.
    """

    text = text.lower()

    # Preserve technical symbols by not removing all punctuation.
    # Replace unwanted characters with spaces.
    text = re.sub(r"[^a-z0-9+#./\s-]", " ", text)

    # Remove repeated whitespace and line breaks.
    text = re.sub(r"\s+", " ", text)

    return text.strip()
