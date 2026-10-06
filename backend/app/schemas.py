from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, ConfigDict, Field


# ============================================================
# AUTH
# ============================================================

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=72)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ============================================================
# JOB APPLICATION
# ============================================================

class JobCreate(BaseModel):
    company: str = Field(min_length=1, max_length=150)
    role: str = Field(min_length=1, max_length=150)
    location: Optional[str] = None
    job_url: Optional[str] = None
    source: Optional[str] = None

    # Kept for frontend compatibility.
    # Backend will always create new applications as Applied.
    status: str = "Applied"

    applied_date: date = Field(default_factory=date.today)
    salary: Optional[str] = None
    notes: Optional[str] = None

    required_skills: List[str] = Field(
        default_factory=list
    )

    resume_version_id: Optional[int] = None


class JobOut(JobCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# ============================================================
# INTERVIEW
# ============================================================

class InterviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_id: int
    round_name: str
    interview_date: datetime
    interviewer: Optional[str] = None
    type: Optional[str] = None
    notes: Optional[str] = None
    result: str


# ============================================================
# COMPANY
# ============================================================

class CompanyCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    email: EmailStr


class CompanyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    created_at: datetime


# ============================================================
# COMPANY APPLICATION UPDATE
# ============================================================

class CompanyStatusUpdate(BaseModel):
    status: str = Field(
        min_length=1,
        max_length=40
    )


# ============================================================
# COMPANY INTERVIEW
# ============================================================

class CompanyInterviewCreate(BaseModel):
    round_name: str = Field(
        min_length=1,
        max_length=100
    )

    interview_date: datetime

    interviewer: Optional[str] = Field(
        default=None,
        max_length=150
    )

    type: Optional[str] = Field(
        default=None,
        max_length=80
    )

    notes: Optional[str] = None

    result: str = Field(
        default="Scheduled",
        max_length=40
    )


class CompanyInterviewUpdate(BaseModel):
    round_name: Optional[str] = Field(
        default=None,
        max_length=100
    )

    interview_date: Optional[datetime] = None

    interviewer: Optional[str] = Field(
        default=None,
        max_length=150
    )

    type: Optional[str] = Field(
        default=None,
        max_length=80
    )

    notes: Optional[str] = None

    result: Optional[str] = Field(
        default=None,
        max_length=40
    )


# ============================================================
# RESUME
# ============================================================

class ResumeCreate(BaseModel):
    name: str
    skills: List[str] = Field(default_factory=list)


class ResumeOut(ResumeCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    file_name: Optional[str]
    created_at: datetime


# ============================================================
# SKILL GAP
# ============================================================

class SkillGapRequest(BaseModel):
    job_id: int


# ============================================================
# JOB DESCRIPTION
# ============================================================

class JobDescriptionCreate(BaseModel):
    job_id: Optional[int] = None
    title: Optional[str] = None
    text: str = Field(
        min_length=30,
        max_length=30000
    )


# ============================================================
# MATCH
# ============================================================

class MatchRequest(BaseModel):
    resume_id: int
    job_id: Optional[int] = None
    job_description_id: Optional[int] = None