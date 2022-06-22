import sys

sys.path.append("..")

import datetime as dt
from typing import Optional

from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from models import Users
from passlib.context import CryptContext
from schemas import UserSchema
from sqlalchemy.orm import Session

SECRET_KEY = "KlgH6AzYDeZeGwD288to79I3vTHT8wp7"
ALGORITHM = "HS256"


router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> str:
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db) -> Users:
    user = db.query(Users).filter(Users.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
    username: str,
    user_id: int,
    expires_delta: Optional[dt.timedelta] = None,
) -> str:
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = dt.datetime.utcnow() + expires_delta
    else:
        expire = dt.datetime.utcnow() + dt.timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    token: str = Depends(oauth2_bearer),
) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise get_auth_exception("Could not validate credentials")
        return {"username": username, "id": user_id}
    except JWTError:
        raise get_auth_exception("Could not validate credentials")


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> dict:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise get_auth_exception("Incorrect username or password")
    token = create_access_token(
        user.username,
        user.id,
        expires_delta=dt.timedelta(minutes=20),
    )
    return {"token": token}


# Exceptions
def get_auth_exception(msg: str = "Could not validate credentials") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=msg,
        headers={"WWW-Authenticate": "Bearer"},
    )
