import hashlib
import secrets

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Company


router = APIRouter(
    prefix="/company",
    tags=["Company Integration"],
)


# ============================================================
# API KEY HELPERS
# ============================================================

def hash_api_key(api_key: str) -> str:
    """
    Convert the company's raw API key into a SHA-256 hash.

    Only the hash is stored in PostgreSQL.
    The original API key is shown only when it is created.
    """
    return hashlib.sha256(
        api_key.encode("utf-8")
    ).hexdigest()


def generate_api_key() -> str:
    """
    Generate a secure company API key.
    """
    return (
        "jt_live_"
        + secrets.token_urlsafe(32)
    )


# ============================================================
# COMPANY AUTHENTICATION
# ============================================================

def get_company_from_api_key(
    x_api_key: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    """
    Authenticate a company using the X-API-Key header.
    """

    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="Company API key is required.",
        )

    api_key_hash = hash_api_key(x_api_key)

    company = (
        db.query(Company)
        .filter(
            Company.api_key_hash == api_key_hash
        )
        .first()
    )

    if not company:
        raise HTTPException(
            status_code=401,
            detail="Invalid company API key.",
        )

    return company


# ============================================================
# CREATE COMPANY
# ============================================================

@router.post("/register")
def register_company(
    name: str,
    email: str | None = None,
    db: Session = Depends(get_db),
):
    """
    Register a company and generate its API key.

    IMPORTANT:
    This endpoint is intended for development/testing.
    Later we can protect company registration with an admin system.
    """

    existing = (
        db.query(Company)
        .filter(
            Company.name == name
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Company already exists.",
        )

    api_key = generate_api_key()

    company = Company(
        name=name.strip(),
        email=email.strip() if email else None,
        api_key_hash=hash_api_key(api_key),
    )

    db.add(company)
    db.commit()
    db.refresh(company)

    return {
        "message": "Company registered successfully.",
        "company_id": company.id,
        "company_name": company.name,
        "api_key": api_key,
    }


# ============================================================
# TEST COMPANY AUTHENTICATION
# ============================================================

@router.get("/me")
def company_me(
    company: Company = Depends(
        get_company_from_api_key
    ),
):
    """
    Test endpoint for company authentication.
    """

    return {
        "authenticated": True,
        "company_id": company.id,
        "company_name": company.name,
        "email": company.email,
    }