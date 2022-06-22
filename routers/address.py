import sys

sys.path.append("..")

from models import Address
from database import SessionLocal
from fastapi import APIRouter, Depends
from schemas import AddressSchema
from sqlalchemy.orm import Session

from .auth import get_auth_exception, get_current_user

router = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post("/")
async def create_address(
    address_data: AddressSchema,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user is None:
        raise get_user_exception()
    address = Address()
    address.address1 = address_data.address1
    address.address2 = address_data.address2
    address.city = address_data.city
    address.state = address_data.state
    address.country = address_data.country
    address.postalcode = address_data.postalcode
    address.user_id = user.get("id")

    db.add(address)

    # NOTE: If the relationship where inverse
    # db.flush()
    # user_model = (
    #     db.query(Users).filter(Users.id == user.get("id")).first()
    # )
    # user_model.address_id = address.id
    # db.add(user_model)

    db.commit()

    return successful_response(200)


def successful_response(status_code: int) -> dict:
    return {"status_code": status_code, "transaction": "Succesful"}
