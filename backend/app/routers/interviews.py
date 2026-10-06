from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import Interview, JobApplication
from ..schemas import InterviewOut


router = APIRouter(
    prefix="/interviews",
    tags=["Interviews"],
)


# =========================================================
# GET ALL CURRENT INTERVIEWS
# =========================================================

@router.get("", response_model=list[InterviewOut])
def list_interviews(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Return interviews only for applications that are
    currently in the Interview stage.

    If the company changes an application to:
        Offer
        Rejected
        Withdrawn

    the old interview record remains in the database,
    but it is no longer shown as an active interview.
    """

    return (
        db.query(Interview)
        .join(
            JobApplication,
            Interview.job_id == JobApplication.id,
        )
        .filter(
            JobApplication.user_id == user.id,
            JobApplication.status == "Interview",
        )
        .order_by(
            Interview.interview_date
        )
        .all()
    )


# =========================================================
# GET ONE CURRENT INTERVIEW
# =========================================================

@router.get(
    "/{interview_id}",
    response_model=InterviewOut,
)
def get_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Return one interview only if its application is
    currently in the Interview stage.
    """

    interview = (
        db.query(Interview)
        .join(
            JobApplication,
            Interview.job_id == JobApplication.id,
        )
        .filter(
            Interview.id == interview_id,
            JobApplication.user_id == user.id,
            JobApplication.status == "Interview",
        )
        .first()
    )

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found",
        )

    return interview