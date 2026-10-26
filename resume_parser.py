
from pathlib import Path
from pypdf import PdfReader
from docx import Document


def extract_resume_text(file_path):
    """
    Extract text from a PDF or DOCX resume.
    file_path: Path to the resume file.
    """

    path = Path(file_path)
    extension = path.suffix.lower()

    if not path.exists():
        raise FileNotFoundError(f"Resume file not found: {path}")

    if extension == ".pdf":
        reader = PdfReader(str(path))
        text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    elif extension == ".docx":
        document = Document(str(path))
        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    else:
        raise ValueError(
            "Unsupported file format. Please use PDF or DOCX."
        )

    if not text.strip():
        raise ValueError(
            "No readable text found. The resume may be scanned."
        )

    return text
