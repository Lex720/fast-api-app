import sys

sys.path.append("..")

from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException, status
from models import Users
from schemas import UserSchema, UserVerificationSchema
from sqlalchemy.orm import Session

from .auth import (
    get_auth_exception,
    get_current_user,
    get_password_hash,
    verify_password,
)

router = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/")
async def read_all(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
) -> list:
    return db.query(Users).all()


@router.get("/{user_id}/")
async def read_user(
    user_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    user_instance = db.query(Users).filter(Users.id == user_id).first()
    if not user_instance:
        raise http_exception()
    return user_instance


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserSchema,
    # user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    user_instance = Users()
    user_instance.email = user_data.email
    user_instance.username = user_data.username
    user_instance.first_name = user_data.first_name
    user_instance.last_name = user_data.last_name
    user_instance.hashed_password = get_password_hash(user_data.password)
    user_instance.is_active = True
    user_instance.phone_number = user_data.phone_number
    db.add(user_instance)
    db.commit()
    return successful_response(200)


@router.put("/update_password/")
async def update_user_password(
    user_data: UserVerificationSchema,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    if user is None:
        raise get_auth_exception()
    user_instance = db.query(Users).filter(Users.id == user.get("id")).first()
    if not user_instance:
        raise http_exception()
    if user_data.username == user_instance.username and verify_password(
        user_data.password, user_instance.hashed_password
    ):
        user_instance.hashed_password = get_password_hash(user_data.new_password)
        db.add(user_instance)
        db.commit()
        return successful_response(200)
    raise http_exception()


@router.put("/{user_id}/")
async def update_user(
    user_id: int,
    user_data: UserSchema,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    user_instance = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise http_exception()
    user_instance.email = user_data.email
    user_instance.username = user_data.username
    user_instance.first_name = user_data.first_name
    user_instance.last_name = user_data.last_name
    user_instance.is_active = user_data.is_active or True
    user_instance.phone_number = user_data.phone_number
    db.add(user_instance)
    db.commit()
    return successful_response(200)


@router.delete("/{user_id}/")
async def delete_user(
    user_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> str:
    user_instance = (
        db.query(Users)
        .filter(Users.id == user_id)
        .first()
    )
    if not user_instance:
        raise http_exception()
    db.query(Users).filter(Users.id == user_id).delete()
    db.commit()
    return successful_response(200)


def successful_response(status_code: int) -> dict:
    return {"status_code": status_code, "transaction": "Succesful"}


# Exceptions
def http_exception() -> HTTPException:
    return HTTPException(
        status_code=422,
        detail=[
            {
                "loc": ["string", 0],
                "msg": "User not found",
                "type": "string",
            }
        ],
    )
