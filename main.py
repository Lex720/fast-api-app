from fastapi import Depends, FastAPI

from company.companyapis import router as companyapis_router
from company.dependencies import get_token_header
from database import Base, engine
from routers.auth import router as auth_router
from routers.todos import router as todos_router
from routers.users import router as users_router
from routers.address import router as address_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["auth"],
    responses={401: {"user": "Not authorized"}},
)
app.include_router(
    todos_router,
    prefix="/todos",
    tags=["todos"],
    responses={404: {"user": "Not found"}},
)
app.include_router(
    users_router,
    prefix="/users",
    tags=["users"],
    responses={404: {"user": "Not found"}},
)
app.include_router(
    address_router,
    prefix="/address",
    tags=["address"],
    responses={404: {"address": "Not found"}},
)
app.include_router(
    companyapis_router,
    prefix="/companyapis",
    tags=["companyapis"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "Internal use only"}},
)
