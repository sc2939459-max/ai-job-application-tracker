from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserLogin, Token, UserOut
from ..auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email.lower()).first():
        raise HTTPException(400, "Email already registered")
    user = User(name=data.name, email=data.email.lower(), password_hash=hash_password(data.password))
    db.add(user); db.commit(); db.refresh(user)
    return Token(access_token=create_access_token(user.id), user=user)

@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email.lower()).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Incorrect email or password")
    return Token(access_token=create_access_token(user.id), user=user)
@router.post("/swagger-login", response_model=Token)
def swagger_login(
    data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.email == data.username.lower())
        .first()
    )

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    return Token(
        access_token=create_access_token(user.id),
        user=user,
    )

@router.get("/me", response_model=UserOut)
def me(user=Depends(__import__("app.deps", fromlist=["get_current_user"]).get_current_user)):
    return user
