from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import JobApplication, ResumeVersion
from ..schemas import SkillGapRequest


router = APIRouter(prefix="/skills", tags=["Skill Gap"])


def normalize_skill(skill: str) -> str:
    """
    Normalize a skill so Python, python and PYTHON
    are treated as the same skill.
    """
    return " ".join(skill.strip().lower().split())


@router.post("/gap")
def skill_gap(
    data: SkillGapRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    job = db.get(JobApplication, data.job_id)

    if not job or job.user_id != user.id:
        raise HTTPException(404, "Job not found")

    # Collect and normalize skills from all user's resume versions.
    resume_skills = set()

    resumes = (
        db.query(ResumeVersion)
        .filter(ResumeVersion.user_id == user.id)
        .all()
    )

    for resume in resumes:
        for skill in (resume.skills or []):
            if skill and str(skill).strip():
                resume_skills.add(
                    normalize_skill(str(skill))
                )

    # Normalize required skills from the saved job.
    required = {
        normalize_skill(str(skill))
        for skill in (job.required_skills or [])
        if skill and str(skill).strip()
    }

    matched = sorted(required & resume_skills)
    missing = sorted(required - resume_skills)

    score = (
        round(len(matched) / len(required) * 100, 1)
        if required
        else 100
    )

    return {
        "job_id": job.id,
        "required_skills": sorted(required),
        "matched_skills": matched,
        "missing_skills": missing,
        "match_percentage": score,
    }