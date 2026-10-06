import re

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user

from ..models import (
    JobApplication,
    JobDescription,
    MatchAnalysis,
    ResumeAnalysis,
    ResumeVersion,
)

from ..schemas import (
    JobDescriptionCreate,
    MatchRequest,
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/ai",
    tags=["AI Analysis"],
)


# ============================================================
# SKILL ALIASES
# ============================================================

SKILL_ALIASES: dict[str, list[str]] = {

    # ========================================================
    # PROGRAMMING LANGUAGES
    # ========================================================

    "python": [
        "python",
    ],

    "java": [
        "java",
    ],

    "javascript": [
        "javascript",
        "java script",
        "js",
    ],

    "typescript": [
        "typescript",
        "type script",
        "ts",
    ],

    "c++": [
        "c++",
        "cpp",
    ],

    "c#": [
        "c#",
        "c sharp",
        "csharp",
    ],

    "php": [
        "php",
    ],

    "ruby": [
        "ruby",
    ],

    "kotlin": [
        "kotlin",
    ],

    "swift": [
        "swift",
    ],

    "go": [
        "golang",
        "go language",
        "go programming",
    ],

    # ========================================================
    # FRONTEND
    # ========================================================

    "html": [
        "html",
        "html5",
    ],

    "css": [
        "css",
        "css3",
    ],

    "react": [
        "react",
        "react.js",
        "reactjs",
        "react js",
    ],

    "next.js": [
        "next.js",
        "nextjs",
        "next js",
    ],

    "angular": [
        "angular",
        "angular.js",
        "angularjs",
    ],

    "vue": [
        "vue",
        "vue.js",
        "vuejs",
    ],

    "bootstrap": [
        "bootstrap",
    ],

    "tailwind css": [
        "tailwind",
        "tailwind css",
        "tailwindcss",
    ],

    "chart.js": [
        "chart.js",
        "chartjs",
    ],

    # ========================================================
    # BACKEND / FRAMEWORKS
    # ========================================================

    "node.js": [
        "node.js",
        "nodejs",
        "node js",
    ],

    "express": [
        "express",
        "express.js",
        "expressjs",
    ],

    "fastapi": [
        "fastapi",
        "fast api",
    ],

    "django": [
        "django",
    ],

    "flask": [
        "flask",
    ],

    "spring": [
        "spring",
    ],

    "spring boot": [
        "spring boot",
        "springboot",
    ],

    "streamlit": [
        "streamlit",
    ],

    # ========================================================
    # DATABASES
    # ========================================================

    "sql": [
        "sql",
        "structured query language",
    ],

    "mysql": [
        "mysql",
        "my sql",
    ],

    "postgresql": [
        "postgresql",
        "postgres",
        "postgre sql",
    ],

    "mongodb": [
        "mongodb",
        "mongo db",
        "mongo",
    ],

    "sqlite": [
        "sqlite",
        "sqlite3",
    ],

    "oracle": [
        "oracle database",
        "oracle db",
        "oracle",
    ],

    "redis": [
        "redis",
    ],

    # ========================================================
    # DATA SCIENCE / ANALYTICS
    # ========================================================

    "pandas": [
        "pandas",
    ],

    "numpy": [
        "numpy",
        "num py",
    ],

    "scikit-learn": [
        "scikit-learn",
        "scikit learn",
        "sklearn",
    ],

    "matplotlib": [
        "matplotlib",
    ],

    "seaborn": [
        "seaborn",
    ],

    "plotly": [
        "plotly",
    ],

    "data science": [
        "data science",
    ],

    "data analysis": [
        "data analysis",
        "data analytics",
    ],

    "data visualization": [
        "data visualization",
        "data visualisation",
    ],

    "statistics": [
        "statistics",
        "statistical analysis",
    ],

    "excel": [
        "excel",
        "microsoft excel",
        "ms excel",
    ],

    "power bi": [
        "power bi",
        "powerbi",
        "power-bi",
    ],

    "tableau": [
        "tableau",
    ],

    "etl": [
        "etl",
        "extract transform load",
    ],

    # ========================================================
    # MACHINE LEARNING / AI
    # ========================================================

    "machine learning": [
        "machine learning",
        "machine-learning",
    ],

    "deep learning": [
        "deep learning",
        "deep-learning",
    ],

    "artificial intelligence": [
        "artificial intelligence",
        "artificial-intelligence",
    ],

    "tensorflow": [
        "tensorflow",
    ],

    "pytorch": [
        "pytorch",
        "py torch",
    ],

    "nlp": [
        "nlp",
        "natural language processing",
    ],

    "computer vision": [
        "computer vision",
    ],

    "generative ai": [
        "generative ai",
        "generative-ai",
        "gen ai",
    ],

    "llm": [
        "llm",
        "large language model",
        "large language models",
    ],

    "openai": [
        "openai",
        "open ai",
    ],

    "langchain": [
        "langchain",
    ],

    # ========================================================
    # APIS
    # ========================================================

    "rest api": [
        "rest api",
        "rest apis",
        "restful api",
        "restful apis",
        "rest-api",
    ],

    "graphql": [
        "graphql",
        "graph ql",
    ],

    "api": [
        "api",
        "apis",
        "application programming interface",
    ],

    "postman": [
        "postman",
    ],

    # ========================================================
    # VERSION CONTROL / DEVELOPMENT TOOLS
    # ========================================================

    "git": [
        "git",
    ],

    "github": [
        "github",
        "git hub",
    ],

    "gitlab": [
        "gitlab",
        "git lab",
    ],

    "bitbucket": [
        "bitbucket",
    ],

    "jira": [
        "jira",
    ],

    "vs code": [
        "vs code",
        "visual studio code",
    ],

    # ========================================================
    # DEVOPS / CLOUD
    # ========================================================

    "docker": [
        "docker",
        "docker container",
        "docker containers",
    ],

    "kubernetes": [
        "kubernetes",
        "k8s",
    ],

    "aws": [
        "aws",
        "amazon web services",
    ],

    "azure": [
        "azure",
        "microsoft azure",
    ],

    "gcp": [
        "gcp",
        "google cloud",
        "google cloud platform",
    ],

    "linux": [
        "linux",
    ],

    "jenkins": [
        "jenkins",
    ],

    "terraform": [
        "terraform",
    ],

    "ci/cd": [
        "ci/cd",
        "cicd",
        "continuous integration",
        "continuous delivery",
        "continuous deployment",
    ],

    # ========================================================
    # TESTING
    # ========================================================

    "pytest": [
        "pytest",
        "py test",
    ],

    "selenium": [
        "selenium",
    ],

    "unit testing": [
        "unit testing",
        "unit test",
        "unit tests",
    ],

    "software testing": [
        "software testing",
    ],

    # ========================================================
    # SOFTWARE ENGINEERING
    # ========================================================

    "oop": [
        "oop",
        "object oriented programming",
        "object-oriented programming",
    ],

    "data structures": [
        "data structures",
        "data structure",
    ],

    "algorithms": [
        "algorithms",
        "algorithm",
    ],

    "sdlc": [
        "sdlc",
        "software development life cycle",
        "software development lifecycle",
    ],

    "agile": [
        "agile",
    ],

    "scrum": [
        "scrum",
    ],
}


# ============================================================
# JOB DESCRIPTION KEYWORDS
# ============================================================

JOB_KEYWORDS = [

    "bachelor",
    "master",
    "btech",
    "b.tech",
    "mtech",
    "m.tech",
    "degree",

    "internship",
    "intern",

    "fresher",
    "fresh graduate",
    "entry level",

    "experience",
    "years",

    "developer",
    "engineer",
    "analyst",

    "software",
    "backend",
    "frontend",
    "full stack",

    "data",
    "cloud",
    "deployment",

    "testing",
    "database",

    "api",
    "rest",

    "development",
    "programming",
    "application",
]


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(
    text: str | None,
) -> str:

    if not text:
        return ""

    text = str(text)

    text = text.replace(
        "\u00a0",
        " ",
    )

    text = text.replace(
        "\u200b",
        "",
    )

    text = text.replace(
        "\ufeff",
        "",
    )

    text = re.sub(
        r"[\r\n\t]+",
        " ",
        text,
    )

    text = text.casefold()

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


# ============================================================
# JOB DESCRIPTION NORMALIZATION
# ============================================================

def normalize_job_description(
    text: str | None,
) -> str:

    """
    Normalize job-description content so that:

    Python Developer
    python developer
    Python   Developer
    Python Developer\n

    are treated as the same job description.
    """

    return normalize_text(text)


# ============================================================
# SAFE TERM MATCHING
# ============================================================

def contains_term(
    text: str,
    term: str,
) -> bool:

    normalized_text = normalize_text(
        text
    )

    normalized_term = normalize_text(
        term
    )

    if not normalized_text:
        return False

    if not normalized_term:
        return False

    pattern = (
        r"(?<![a-z0-9])"
        + re.escape(normalized_term)
        + r"(?![a-z0-9])"
    )

    return (
        re.search(
            pattern,
            normalized_text,
            flags=re.IGNORECASE,
        )
        is not None
    )


# ============================================================
# EXTRACT SKILLS
# ============================================================

def extract_skills(
    text: str | None,
) -> list[str]:

    normalized = normalize_text(
        text
    )

    if not normalized:
        return []

    detected: set[str] = set()

    for canonical_skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            if contains_term(
                normalized,
                alias,
            ):

                detected.add(
                    canonical_skill
                )

                break

    return sorted(
        detected
    )


# ============================================================
# EXTRACT RESUME SKILLS
# ============================================================

def extract_resume_skills(
    extracted_text: str | None,
    stored_skills: list | None = None,
) -> list[str]:

    detected_from_text = set(
        extract_skills(
            extracted_text
        )
    )

    detected_from_database: set[str] = set()

    if stored_skills:

        for skill in stored_skills:

            if not skill:
                continue

            skill_matches = extract_skills(
                str(skill)
            )

            if skill_matches:

                detected_from_database.update(
                    skill_matches
                )

            else:

                normalized_skill = normalize_text(
                    str(skill)
                )

                if normalized_skill:

                    detected_from_database.add(
                        normalized_skill
                    )

    return sorted(
        detected_from_text
        | detected_from_database
    )


# ============================================================
# EXTRACT JOB KEYWORDS
# ============================================================

def extract_keywords(
    text: str | None,
) -> list[str]:

    normalized = normalize_text(
        text
    )

    if not normalized:
        return []

    found: set[str] = set()

    for keyword in JOB_KEYWORDS:

        if contains_term(
            normalized,
            keyword,
        ):

            found.add(
                keyword
            )

    return sorted(
        found
    )


# ============================================================
# GET OWNED RESUME
# ============================================================

def get_owned_resume(
    db: Session,
    resume_id: int,
    user,
) -> ResumeVersion:

    resume = db.get(
        ResumeVersion,
        resume_id,
    )

    if (
        not resume
        or resume.user_id != user.id
    ):

        raise HTTPException(
            status_code=404,
            detail="Resume not found.",
        )

    return resume


# ============================================================
# GET OWNED JOB
# ============================================================

def get_owned_job(
    db: Session,
    job_id: int | None,
    user,
) -> JobApplication | None:

    if job_id is None:
        return None

    job = db.get(
        JobApplication,
        job_id,
    )

    if (
        not job
        or job.user_id != user.id
    ):

        raise HTTPException(
            status_code=404,
            detail="Job application not found.",
        )

    return job


# ============================================================
# GET OWNED JOB DESCRIPTION
# ============================================================

def get_owned_job_description(
    db: Session,
    job_description_id: int,
    user,
) -> JobDescription:

    job_description = db.get(
        JobDescription,
        job_description_id,
    )

    if (
        not job_description
        or job_description.user_id != user.id
    ):

        raise HTTPException(
            status_code=404,
            detail="Job description not found.",
        )

    return job_description


# ============================================================
# GET RESUME ANALYSIS
# ============================================================

def get_resume_analysis(
    db: Session,
    resume_id: int,
) -> ResumeAnalysis | None:

    return (
        db.query(
            ResumeAnalysis
        )
        .filter(
            ResumeAnalysis.resume_id == resume_id
        )
        .first()
    )


# ============================================================
# BUILD RESUME SUMMARY
# ============================================================

def build_resume_summary(
    skills: list[str],
    extracted_text: str,
) -> str:

    if not extracted_text:

        return (
            "No readable text was extracted "
            "from this resume."
        )

    preview = " ".join(
        extracted_text.split()
    )[:300]

    if skills:

        return (
            f"Detected {len(skills)} "
            f"technical skills: "
            f"{', '.join(skills)}. "
            f"Resume preview: {preview}"
        )

    return (
        "No supported technical skills were "
        "detected automatically. "
        f"Resume preview: {preview}"
    )


# ============================================================
# CALCULATE MATCH SCORE
# ============================================================

def calculate_match_score(
    resume_skills: set[str],
    required_skills: set[str],
    resume_keywords: set[str],
    job_keywords: set[str],
) -> tuple[float, float, float]:

    # --------------------------------------------------------
    # Technical skill score
    # --------------------------------------------------------

    if required_skills:

        matched_count = len(
            resume_skills
            & required_skills
        )

        skill_score = (
            matched_count
            / len(required_skills)
            * 100
        )

    else:

        skill_score = 100.0

    # --------------------------------------------------------
    # Keyword score
    # --------------------------------------------------------

    if job_keywords:

        keyword_matches = (
            resume_keywords
            & job_keywords
        )

        keyword_score = (
            len(keyword_matches)
            / len(job_keywords)
            * 100
        )

    else:

        keyword_score = 100.0

    # --------------------------------------------------------
    # Final score
    # --------------------------------------------------------

    final_score = (
        skill_score * 0.80
        + keyword_score * 0.20
    )

    return (
        round(skill_score, 1),
        round(keyword_score, 1),
        round(final_score, 1),
    )


# ============================================================
# BUILD RECOMMENDATIONS
# ============================================================

def build_recommendations(
    missing_skills: list[str],
    keyword_score: float,
    matched_skills: list[str],
) -> list[str]:

    recommendations: list[str] = []

    if missing_skills:

        displayed_missing = (
            missing_skills[:8]
        )

        recommendations.append(
            "Strengthen or add truthful evidence "
            "for: "
            + ", ".join(
                displayed_missing
            )
            + "."
        )

    if keyword_score < 50:

        recommendations.append(
            "Review the job description terminology "
            "and naturally use relevant terms in your "
            "resume when they accurately describe your "
            "experience."
        )

    elif keyword_score < 75:

        recommendations.append(
            "Improve terminology alignment by "
            "highlighting relevant experience and "
            "projects using language consistent with "
            "the job description."
        )

    if not matched_skills:

        recommendations.append(
            "The resume currently has no detected "
            "technical skills matching the selected "
            "job requirements."
        )

    if (
        matched_skills
        and not missing_skills
    ):

        recommendations.append(
            "The detected technical skills align "
            "with the job requirements. Keep the "
            "most relevant projects and skills "
            "prominent in the resume."
        )

    if not recommendations:

        recommendations.append(
            "Review the job description and ensure "
            "your strongest relevant experience is "
            "clearly demonstrated with measurable "
            "results."
        )

    return recommendations


# ============================================================
# GET RESUME ANALYSIS ENDPOINT
# ============================================================

@router.get(
    "/resume/{resume_id}",
)
def get_resume_analysis_endpoint(
    resume_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    resume = get_owned_resume(
        db,
        resume_id,
        user,
    )

    analysis = get_resume_analysis(
        db,
        resume.id,
    )

    if not analysis:

        raise HTTPException(
            status_code=404,
            detail=(
                "No AI analysis exists "
                "for this resume."
            ),
        )

    detected_skills = extract_resume_skills(
        extracted_text=(
            analysis.extracted_text
            or ""
        ),
        stored_skills=(
            analysis.detected_skills
            or resume.skills
            or []
        ),
    )

    return {

        "resume_id": resume.id,

        "name": resume.name,

        "file_name": resume.file_name,

        "extracted_characters": len(
            analysis.extracted_text
            or ""
        ),

        "detected_skills": detected_skills,

        "skill_count": len(
            detected_skills
        ),

        "summary": analysis.summary,

        "created_at": analysis.created_at,
    }


# ============================================================
# CREATE / ANALYZE JOB DESCRIPTION
# ============================================================

@router.post(
    "/job-description",
)
def analyze_job_description(
    data: JobDescriptionCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    # --------------------------------------------------------
    # Validate text
    # --------------------------------------------------------

    text = (
        data.text or ""
    ).strip()

    if len(text) < 30:

        raise HTTPException(
            status_code=400,
            detail=(
                "Job description must contain "
                "at least 30 characters."
            ),
        )

    # --------------------------------------------------------
    # Verify optional job
    # --------------------------------------------------------

    job = get_owned_job(
        db,
        data.job_id,
        user,
    )

    # --------------------------------------------------------
    # Extract skills and keywords
    # --------------------------------------------------------

    skills = extract_skills(
        text
    )

    keywords = extract_keywords(
        text
    )

    # --------------------------------------------------------
    # Normalize JD for duplicate detection
    # --------------------------------------------------------

    normalized_text = normalize_job_description(
        text
    )

    # --------------------------------------------------------
    # Find existing identical Job Description
    # --------------------------------------------------------
    #
    # Same user + same job + same JD text
    # = reuse existing JobDescription.
    #
    # This prevents a new job_description_id from being
    # created every time the user clicks Analyze.
    # --------------------------------------------------------

    existing_job_descriptions = (
        db.query(
            JobDescription
        )
        .filter(
            JobDescription.user_id == user.id
        )
        .order_by(
            JobDescription.created_at.desc()
        )
        .all()
    )

    job_description = None

    current_job_id = (
        job.id
        if job
        else None
    )

    for existing in existing_job_descriptions:

        existing_normalized = (
            normalize_job_description(
                existing.raw_text or ""
            )
        )

        existing_job_id = existing.job_id

        same_job = (
            existing_job_id == current_job_id
        )

        if (
            existing_normalized == normalized_text
            and same_job
        ):

            job_description = existing
            break

    # --------------------------------------------------------
    # Create only if identical JD does not exist
    # --------------------------------------------------------

    if job_description is None:

        job_description = JobDescription(

            user_id=user.id,

            job_id=current_job_id,

            title=(
                data.title.strip()
                if data.title
                else (
                    job.role
                    if job
                    else "Job Description"
                )
            ),

            raw_text=text,

            detected_skills=skills,
        )

        db.add(
            job_description
        )

    else:

        # Keep the latest detected skills in sync.
        job_description.detected_skills = skills

        # If the user provides a title and the existing
        # description does not have one, use the new title.
        if (
            data.title
            and data.title.strip()
            and not job_description.title
        ):

            job_description.title = (
                data.title.strip()
            )

    # --------------------------------------------------------
    # Update JobApplication required skills
    # --------------------------------------------------------

    if job:

        job.required_skills = skills

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    try:

        db.commit()

        db.refresh(
            job_description
        )

    except Exception as exc:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to save job description: "
                f"{exc}"
            ),
        )

    # --------------------------------------------------------
    # Return
    # --------------------------------------------------------

    return {

        "id": job_description.id,

        "title": job_description.title,

        "job_id": job_description.job_id,

        "detected_skills": skills,

        "skill_count": len(
            skills
        ),

        "keywords": keywords,

        "character_count": len(text),

        "created_at": (
            job_description.created_at
        ),
    }


# ============================================================
# LIST JOB DESCRIPTIONS
# ============================================================

@router.get(
    "/job-descriptions",
)
def list_job_descriptions(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    items = (
        db.query(
            JobDescription
        )
        .filter(
            JobDescription.user_id == user.id
        )
        .order_by(
            JobDescription.created_at.desc()
        )
        .all()
    )

    return [

        {
            "id": item.id,

            "title": item.title,

            "job_id": item.job_id,

            "detected_skills": (
                item.detected_skills
                or []
            ),

            "created_at": (
                item.created_at
            ),
        }

        for item in items
    ]


# ============================================================
# FIND EXISTING MATCH
# ============================================================

def find_existing_match(
    db: Session,
    user_id: int,
    resume_id: int,
    job_id: int | None,
    job_description_id: int | None,
) -> MatchAnalysis | None:

    query = (
        db.query(
            MatchAnalysis
        )
        .filter(
            MatchAnalysis.user_id == user_id,

            MatchAnalysis.resume_id == resume_id,
        )
    )

    # --------------------------------------------------------
    # Job Description
    # --------------------------------------------------------

    if job_description_id is not None:

        query = query.filter(
            MatchAnalysis.job_description_id
            == job_description_id
        )

    else:

        query = query.filter(
            MatchAnalysis.job_description_id.is_(None)
        )

    # --------------------------------------------------------
    # Job
    # --------------------------------------------------------

    if job_id is not None:

        query = query.filter(
            MatchAnalysis.job_id == job_id
        )

    else:

        query = query.filter(
            MatchAnalysis.job_id.is_(None)
        )

    return (
        query
        .order_by(
            MatchAnalysis.created_at.desc()
        )
        .first()
    )


# ============================================================
# MATCH RESUME TO JOB
# ============================================================

@router.post(
    "/match",
)
def match_resume_to_job(
    data: MatchRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    # ========================================================
    # 1. GET RESUME
    # ========================================================

    resume = get_owned_resume(
        db,
        data.resume_id,
        user,
    )

    # ========================================================
    # 2. GET OPTIONAL JOB
    # ========================================================

    job = get_owned_job(
        db,
        data.job_id,
        user,
    )

    # ========================================================
    # 3. GET RESUME ANALYSIS
    # ========================================================

    resume_analysis = get_resume_analysis(
        db,
        resume.id,
    )

    if not resume_analysis:

        raise HTTPException(
            status_code=400,
            detail=(
                "This resume has not been analyzed yet. "
                "Upload the resume through the Resume page "
                "and analyze it first."
            ),
        )

    # ========================================================
    # 4. EXTRACT RESUME SKILLS
    # ========================================================

    resume_skills_list = extract_resume_skills(

        extracted_text=(
            resume_analysis.extracted_text
            or ""
        ),

        stored_skills=(
            resume_analysis.detected_skills
            or resume.skills
            or []
        ),
    )

    resume_skills = {
        normalize_text(skill)
        for skill in resume_skills_list
        if skill
    }

    # ========================================================
    # 5. FIND JOB DESCRIPTION
    # ========================================================

    job_description: JobDescription | None = None

    # --------------------------------------------------------
    # Explicit JobDescription ID
    # --------------------------------------------------------

    if data.job_description_id:

        job_description = (
            get_owned_job_description(
                db,
                data.job_description_id,
                user,
            )
        )

    # --------------------------------------------------------
    # Otherwise get latest JD attached to job
    # --------------------------------------------------------

    elif job:

        job_description = (
            db.query(
                JobDescription
            )
            .filter(
                JobDescription.user_id == user.id,

                JobDescription.job_id == job.id,
            )
            .order_by(
                JobDescription.created_at.desc()
            )
            .first()
        )

    # ========================================================
    # 6. VALIDATE JOB / JD
    # ========================================================

    if (
        not job_description
        and not job
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Select a job or provide a "
                "job description before matching."
            ),
        )

    # ========================================================
    # 7. DETERMINE REQUIRED SKILLS
    # ========================================================

    if job_description:

        source_text = (
            job_description.raw_text
            or ""
        )

        required_skills = set(
            extract_skills(
                source_text
            )
        )

    else:

        source_text = " ".join(
            [
                job.role or "",

                job.company or "",

                job.notes or "",

                " ".join(
                    job.required_skills
                    or []
                ),
            ]
        )

        required_skills = set(
            extract_skills(
                source_text
            )
        )

    # ========================================================
    # 8. MATCHED SKILLS
    # ========================================================

    matched_skills = sorted(
        resume_skills
        & required_skills
    )

    # ========================================================
    # 9. MISSING SKILLS
    # ========================================================

    missing_skills = sorted(
        required_skills
        - resume_skills
    )

    # ========================================================
    # 10. KEYWORD ANALYSIS
    # ========================================================

    job_keywords = set(
        extract_keywords(
            source_text
        )
    )

    resume_text = (
        resume_analysis.extracted_text
        or ""
    )

    resume_keywords = set(
        extract_keywords(
            resume_text
        )
    )

    keyword_matches = sorted(
        resume_keywords
        & job_keywords
    )

    # ========================================================
    # 11. CALCULATE SCORE
    # ========================================================

    (
        skill_score,
        keyword_score,
        final_score,
    ) = calculate_match_score(

        resume_skills=resume_skills,

        required_skills=required_skills,

        resume_keywords=resume_keywords,

        job_keywords=job_keywords,
    )

    # ========================================================
    # 12. BUILD RECOMMENDATIONS
    # ========================================================

    recommendations = build_recommendations(

        missing_skills=missing_skills,

        keyword_score=keyword_score,

        matched_skills=matched_skills,
    )

    # ========================================================
    # 13. DETERMINE MATCH IDENTIFIERS
    # ========================================================

    match_job_id = (
        job.id
        if job
        else (
            job_description.job_id
            if job_description
            else None
        )
    )

    match_job_description_id = (
        job_description.id
        if job_description
        else None
    )

    # ========================================================
    # 14. FIND EXISTING MATCH
    # ========================================================

    match = find_existing_match(

        db=db,

        user_id=user.id,

        resume_id=resume.id,

        job_id=match_job_id,

        job_description_id=(
            match_job_description_id
        ),
    )

    # ========================================================
    # 15. UPDATE OR CREATE
    # ========================================================

    if match:

        # ----------------------------------------------------
        # EXISTING MATCH
        # ----------------------------------------------------

        match.score = final_score

        match.matched_skills = (
            matched_skills
        )

        match.missing_skills = (
            missing_skills
        )

        match.keyword_matches = (
            keyword_matches
        )

        match.recommendations = (
            recommendations
        )

    else:

        # ----------------------------------------------------
        # NEW MATCH
        # ----------------------------------------------------

        match = MatchAnalysis(

            user_id=user.id,

            resume_id=resume.id,

            job_id=match_job_id,

            job_description_id=(
                match_job_description_id
            ),

            score=final_score,

            matched_skills=(
                matched_skills
            ),

            missing_skills=(
                missing_skills
            ),

            keyword_matches=(
                keyword_matches
            ),

            recommendations=(
                recommendations
            ),
        )

        db.add(
            match
        )

    # ========================================================
    # 16. SAVE DATABASE
    # ========================================================

    try:

        db.commit()

        db.refresh(
            match
        )

    except Exception as exc:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to save match analysis: "
                f"{exc}"
            ),
        )

    # ========================================================
    # 17. RETURN RESULT
    # ========================================================

    return {

        "id": match.id,

        "score": final_score,

        "skill_score": skill_score,

        "keyword_score": keyword_score,

        "resume": resume.name,

        "resume_id": resume.id,

        "resume_skills": sorted(
            resume_skills
        ),

        "job": (
            job.role
            if job
            else (
                job_description.title
                if job_description
                else "Job"
            )
        ),

        "company": (
            job.company
            if job
            else None
        ),

        "job_id": match_job_id,

        "job_description_id": (
            match_job_description_id
        ),

        "required_skills": sorted(
            required_skills
        ),

        "matched_skills": (
            matched_skills
        ),

        "missing_skills": (
            missing_skills
        ),

        "keyword_matches": (
            keyword_matches
        ),

        "recommendations": (
            recommendations
        ),

        "created_at": (
            match.created_at
        ),
    }


# ============================================================
# LIST MATCH RESULTS
# ============================================================

@router.get(
    "/matches",
)
def list_matches(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    items = (
        db.query(
            MatchAnalysis
        )
        .filter(
            MatchAnalysis.user_id == user.id
        )
        .order_by(
            MatchAnalysis.created_at.desc()
        )
        .limit(100)
        .all()
    )

    # --------------------------------------------------------
    # Remove duplicate combinations from UI
    # --------------------------------------------------------
    #
    # Identity:
    #
    #   resume_id
    #   job_id
    #   job_description_id
    #
    # Newest record wins.
    # --------------------------------------------------------

    unique_items = []

    seen_keys = set()

    for item in items:

        key = (
            item.resume_id,

            item.job_id,

            item.job_description_id,
        )

        if key in seen_keys:
            continue

        seen_keys.add(
            key
        )

        unique_items.append(
            item
        )

        if len(unique_items) >= 50:
            break

    # --------------------------------------------------------
    # Return
    # --------------------------------------------------------

    return [

        {
            "id": item.id,

            "score": item.score,

            "resume_id": item.resume_id,

            "job_id": item.job_id,

            "job_description_id": (
                item.job_description_id
            ),

            "matched_skills": (
                item.matched_skills
                or []
            ),

            "missing_skills": (
                item.missing_skills
                or []
            ),

            "keyword_matches": (
                item.keyword_matches
                or []
            ),

            "recommendations": (
                item.recommendations
                or []
            ),

            "created_at": (
                item.created_at
            ),
        }

        for item in unique_items
    ]


# ============================================================
# GET SINGLE MATCH RESULT
# ============================================================

@router.get(
    "/matches/{match_id}",
)
def get_match(
    match_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    match = (
        db.query(
            MatchAnalysis
        )
        .filter(

            MatchAnalysis.id == match_id,

            MatchAnalysis.user_id == user.id,
        )
        .first()
    )

    if not match:

        raise HTTPException(
            status_code=404,
            detail="Match analysis not found.",
        )

    return {

        "id": match.id,

        "score": match.score,

        "resume_id": match.resume_id,

        "job_id": match.job_id,

        "job_description_id": (
            match.job_description_id
        ),

        "matched_skills": (
            match.matched_skills
            or []
        ),

        "missing_skills": (
            match.missing_skills
            or []
        ),

        "keyword_matches": (
            match.keyword_matches
            or []
        ),

        "recommendations": (
            match.recommendations
            or []
        ),

        "created_at": (
            match.created_at
        ),
    }