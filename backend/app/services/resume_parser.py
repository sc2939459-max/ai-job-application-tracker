from pathlib import Path

from pypdf import PdfReader


KNOWN_SKILLS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "html",
    "css",
    "react",
    "node.js",
    "nodejs",
    "fastapi",
    "django",
    "flask",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "machine learning",
    "deep learning",
    "data science",
    "data analysis",
    "power bi",
    "tableau",
    "excel",
    "git",
    "github",
    "docker",
    "aws",
    "azure",
    "gcp",
    "rest api",
    "rest apis",
    "api",
    "spring",
    "spring boot",
    "c++",
    "c#",
]


def extract_text_from_pdf(
    file_path: str,
) -> str:
    """
    Extract text from a PDF resume.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Resume file not found: {file_path}"
        )

    reader = PdfReader(
        str(path)
    )

    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)

    resume_text = "\n".join(
        pages
    ).strip()

    if not resume_text:
        raise ValueError(
            "Could not extract text from this PDF."
        )

    return resume_text


def detect_skills(
    text: str,
) -> list[str]:
    """
    Detect known technical skills
    from extracted resume text.
    """

    normalized_text = text.lower()

    detected = []

    for skill in KNOWN_SKILLS:
        if skill.lower() in normalized_text:
            detected.append(skill)

    return sorted(
        set(detected)
    )