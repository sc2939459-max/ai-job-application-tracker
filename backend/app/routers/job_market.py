import os
import re
from collections import Counter
from statistics import mean

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import ResumeVersion


router = APIRouter(prefix="/job-market", tags=["Job Market"])


ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")


COUNTRY_CODES = {
    "India": "in",
    "United Kingdom": "gb",
    "United States": "us",
    "Canada": "ca",
    "Australia": "au",
    "Germany": "de",
    "France": "fr",
    "Ireland": "ie",
    "Netherlands": "nl",
    "Singapore": "sg",
    "New Zealand": "nz",
    "South Africa": "za",
    "Brazil": "br",
    "Mexico": "mx",
}


COMMON_SKILLS = [
    "Python",
    "SQL",
    "JavaScript",
    "TypeScript",
    "React",
    "Angular",
    "Vue",
    "Node.js",
    "FastAPI",
    "Django",
    "Flask",
    "Java",
    "Spring Boot",
    "C++",
    "C#",
    ".NET",
    "AWS",
    "Azure",
    "GCP",
    "Docker",
    "Kubernetes",
    "Git",
    "GitHub",
    "PostgreSQL",
    "MySQL",
    "MongoDB",
    "Redis",
    "Pandas",
    "NumPy",
    "Power BI",
    "Tableau",
    "Excel",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "Machine Learning",
    "Data Science",
    "REST API",
    "GraphQL",
    "Linux",
]


# ---------------------------------------------------------
# SKILL NORMALIZATION
# ---------------------------------------------------------

def normalize_skill(skill: str) -> str:
    """
    Convert different representations of the same skill
    into a comparable form.
    """

    value = str(skill).strip().lower()

    value = re.sub(r"\s+", " ", value)

    aliases = {
        "node js": "node.js",
        "nodejs": "node.js",
        "reactjs": "react",
        "react js": "react",
        "angularjs": "angular",
        "vuejs": "vue",
        "postgres": "postgresql",
        "postgre sql": "postgresql",
        "mysql database": "mysql",
        "powerbi": "power bi",
        "scikit learn": "scikit-learn",
        "sklearn": "scikit-learn",
        "machine-learning": "machine learning",
        "data-science": "data science",
        "rest": "rest api",
        "restful api": "rest api",
    }

    return aliases.get(value, value)


def extract_skills(text: str) -> list[str]:
    """
    Extract known technical skills from job title + description.
    """

    text_lower = text.lower()
    found = []

    for skill in COMMON_SKILLS:
        pattern = re.escape(skill.lower())

        if re.search(
            rf"(?<!\w){pattern}(?!\w)",
            text_lower,
        ):
            found.append(skill)

    return sorted(set(found))


# ---------------------------------------------------------
# NORMALIZE ADZUNA JOB
# ---------------------------------------------------------

def normalize_job(job: dict) -> dict:

    location = job.get("location") or {}
    company = job.get("company") or {}

    description = job.get("description") or ""

    combined_text = (
        f"{job.get('title', '')} "
        f"{description}"
    )

    return {
        "id": str(job.get("id", "")),
        "title": job.get("title") or "Untitled Job",
        "company": (
            company.get("display_name")
            or "Unknown Company"
        ),
        "location": (
            location.get("display_name")
            or "Location not specified"
        ),
        "description": description,
        "salary_min": job.get("salary_min"),
        "salary_max": job.get("salary_max"),
        "salary_predicted": bool(
            job.get("salary_is_predicted")
        ),
        "contract_type": job.get("contract_type"),
        "contract_time": job.get("contract_time"),
        "created": job.get("created"),
        "category": (
            job.get("category") or {}
        ).get("label"),
        "url": job.get("redirect_url"),
        "skills": extract_skills(combined_text),
        "source": "Adzuna",
    }


# ---------------------------------------------------------
# FETCH ADZUNA
# ---------------------------------------------------------

async def fetch_adzuna_jobs(
    query: str,
    location: str,
    country: str,
    page: int = 1,
    results_per_page: int = 20,
    salary_min: int | None = None,
) -> dict:

    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        raise HTTPException(
            status_code=503,
            detail=(
                "Job market API is not configured. "
                "Add ADZUNA_APP_ID and ADZUNA_APP_KEY "
                "to backend/.env."
            ),
        )

    country_code = COUNTRY_CODES.get(country)

    if not country_code:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported country: {country}",
        )

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": results_per_page,
        "content-type": "application/json",
    }

    if query.strip():
        params["what"] = query.strip()

    if location.strip():
        params["where"] = location.strip()

    if salary_min is not None:
        params["salary_min"] = salary_min

    url = (
        f"https://api.adzuna.com/v1/api/jobs/"
        f"{country_code}/search/{page}"
    )

    try:
        async with httpx.AsyncClient(
            timeout=15
        ) as client:

            response = await client.get(
                url,
                params=params,
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail=(
                    "Job market provider "
                    "returned an error."
                ),
            )

        return response.json()

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail=(
                "Job market provider timed out."
            ),
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail=(
                "Unable to reach job market provider."
            ),
        )


# ---------------------------------------------------------
# SEARCH JOBS
# ---------------------------------------------------------

@router.get("/search")
async def search_jobs(
    query: str = Query("", max_length=100),
    location: str = Query("", max_length=100),
    country: str = Query("India"),
    page: int = Query(1, ge=1, le=50),
    results_per_page: int = Query(
        20,
        ge=1,
        le=50,
    ),
    salary_min: int | None = Query(
        None,
        ge=0,
    ),
    user=Depends(get_current_user),
):

    data = await fetch_adzuna_jobs(
        query=query,
        location=location,
        country=country,
        page=page,
        results_per_page=results_per_page,
        salary_min=salary_min,
    )

    jobs = [
        normalize_job(job)
        for job in data.get("results", [])
    ]

    return {
        "source": "Adzuna",
        "country": country,
        "query": query,
        "location": location,
        "count": len(jobs),
        "total": data.get(
            "count",
            len(jobs),
        ),
        "jobs": jobs,
    }


# ---------------------------------------------------------
# MARKET INSIGHTS + RESUME MATCH
# ---------------------------------------------------------

@router.get("/insights")
async def market_insights(
    query: str = Query("", max_length=100),
    location: str = Query("", max_length=100),
    country: str = Query("India"),
    page: int = Query(1, ge=1, le=50),
    results_per_page: int = Query(
        50,
        ge=1,
        le=50,
    ),
    resume_id: int | None = Query(None, ge=1),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    # -----------------------------------------------------
    # FETCH JOBS
    # -----------------------------------------------------

    data = await fetch_adzuna_jobs(
        query=query,
        location=location,
        country=country,
        page=page,
        results_per_page=results_per_page,
    )

    raw_jobs = data.get("results", [])

    jobs = [
        normalize_job(job)
        for job in raw_jobs
    ]

    analyzed_jobs = len(jobs)

    # -----------------------------------------------------
    # MARKET SKILLS
    # -----------------------------------------------------

    skill_counter = Counter()

    for job in jobs:
        for skill in job["skills"]:
            skill_counter[skill] += 1

    top_skills = []

    for skill, count in skill_counter.most_common():

        percentage = (
            round(
                (count / analyzed_jobs) * 100
            )
            if analyzed_jobs
            else 0
        )

        top_skills.append({
            "skill": skill,
            "count": count,
            "percentage": percentage,
        })

    # -----------------------------------------------------
    # TOP COMPANIES
    # -----------------------------------------------------

    company_counter = Counter(
        job["company"]
        for job in jobs
        if (
            job["company"]
            and job["company"] != "Unknown Company"
        )
    )

    top_companies = [
        {
            "company": company,
            "count": count,
        }
        for company, count
        in company_counter.most_common(10)
    ]

    # -----------------------------------------------------
    # SALARY
    # -----------------------------------------------------

    salary_mins = [
        job["salary_min"]
        for job in jobs
        if isinstance(
            job["salary_min"],
            (int, float),
        )
        and job["salary_min"] > 0
    ]

    salary_maxs = [
        job["salary_max"]
        for job in jobs
        if isinstance(
            job["salary_max"],
            (int, float),
        )
        and job["salary_max"] > 0
    ]

    average_salary_min = (
        round(mean(salary_mins), 2)
        if salary_mins
        else None
    )

    average_salary_max = (
        round(mean(salary_maxs), 2)
        if salary_maxs
        else None
    )

    # -----------------------------------------------------
    # CONTRACT TYPES
    # -----------------------------------------------------

    contract_counter = Counter(
        job["contract_time"]
        for job in jobs
        if job["contract_time"]
    )

    contract_types = [
        {
            "type": contract_type,
            "count": count,
        }
        for contract_type, count
        in contract_counter.most_common()
    ]

    # -----------------------------------------------------
    # USER RESUME
    # -----------------------------------------------------

    if resume_id is not None:
        latest_resume = (
            db.query(ResumeVersion)
            .filter(
                ResumeVersion.id == resume_id,
                ResumeVersion.user_id == user.id,
            )
            .first()
        )
        if not latest_resume:
            raise HTTPException(
                status_code=404,
                detail="Selected resume not found",
            )
    else:
        latest_resume = (
            db.query(ResumeVersion)
            .filter(
                ResumeVersion.user_id == user.id
            )
            .order_by(
                ResumeVersion.created_at.desc()
            )
            .first()
        )

    resume_skills_raw = (
        latest_resume.skills
        if latest_resume
        else []
    )

    resume_skill_map = {}

    for skill in resume_skills_raw or []:

        if not skill:
            continue

        original = str(skill).strip()

        if not original:
            continue

        normalized = normalize_skill(original)

        resume_skill_map[normalized] = original

    resume_skill_keys = set(
        resume_skill_map.keys()
    )

    # -----------------------------------------------------
    # MARKET SKILL MATCHING
    # -----------------------------------------------------

    market_skill_map = {}

    for skill in COMMON_SKILLS:

        normalized = normalize_skill(skill)

        market_skill_map[normalized] = skill

    market_skill_keys = {
        normalize_skill(skill)
        for skill in skill_counter.keys()
    }

    matched_skill_keys = (
        market_skill_keys
        & resume_skill_keys
    )

    missing_skill_keys = (
        market_skill_keys
        - resume_skill_keys
    )

    matched_skills = sorted(
        [
            market_skill_map.get(
                skill,
                skill,
            )
            for skill in matched_skill_keys
        ]
    )

    missing_skills = sorted(
        [
            market_skill_map.get(
                skill,
                skill,
            )
            for skill in missing_skill_keys
        ],
        key=lambda skill: (
            -skill_counter.get(
                skill,
                skill_counter.get(
                    next(
                        (
                            s
                            for s in skill_counter
                            if normalize_skill(s)
                            == normalize_skill(skill)
                        ),
                        "",
                    ),
                    0,
                ),
            ),
            skill.lower(),
        ),
    )

    # -----------------------------------------------------
    # RESUME MATCH SCORE
    # -----------------------------------------------------

    total_market_skills = len(
        market_skill_keys
    )

    match_percentage = (
        round(
            (
                len(matched_skill_keys)
                / total_market_skills
            )
            * 100,
            1,
        )
        if total_market_skills
        else 0
    )

    # -----------------------------------------------------
    # RECOMMENDATIONS
    # -----------------------------------------------------

    recommendations = []

    # Recommend highest-demand missing skills first.
    missing_with_counts = []

    for skill_key in missing_skill_keys:

        display_skill = market_skill_map.get(
            skill_key,
            skill_key,
        )

        count = 0

        for market_skill, skill_count in skill_counter.items():

            if normalize_skill(market_skill) == skill_key:
                count = skill_count
                break

        missing_with_counts.append(
            (
                display_skill,
                count,
            )
        )

    missing_with_counts.sort(
        key=lambda item: (
            -item[1],
            item[0].lower(),
        )
    )

    for skill, count in missing_with_counts[:5]:

        percentage = (
            round(
                (count / analyzed_jobs) * 100
            )
            if analyzed_jobs
            else 0
        )

        recommendations.append({
            "skill": skill,
            "jobs_requiring_skill": count,
            "market_percentage": percentage,
            "message": (
                f"{skill} appears in "
                f"{percentage}% of the analyzed "
                f"job listings."
            ),
        })

    # -----------------------------------------------------
    # RESPONSE
    # -----------------------------------------------------

    return {
        "source": "Adzuna",

        "search": {
            "query": query,
            "location": location,
            "country": country,
            "page": page,
            "resume_id": resume_id,
        },

        "total_jobs_available": data.get(
            "count",
            analyzed_jobs,
        ),

        "jobs_analyzed": analyzed_jobs,

        "top_skills": top_skills,

        "top_companies": top_companies,

        "salary": {
            "average_min": average_salary_min,
            "average_max": average_salary_max,
            "jobs_with_salary": max(
                len(salary_mins),
                len(salary_maxs),
            ),
        },

        "contract_types": contract_types,

        "resume_match": {
            "resume_id": (
                latest_resume.id
                if latest_resume
                else None
            ),
            "resume_name": (
                latest_resume.name
                if latest_resume
                else None
            ),
            "resume_skills": sorted(
                resume_skill_keys
            ),
            "match_percentage": (
                match_percentage
            ),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "recommendations": recommendations,
        },
    }