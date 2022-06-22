import sys

sys.path.append("..")

from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException, status
from models import Todos
from schemas import TodoSchema
from sqlalchemy.orm import Session

from .auth import get_auth_exception, get_current_user

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
    return db.query(Todos).all()


@router.get("/user/")
async def read_all_by_user(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Todos]:
    if user is None:
        raise get_auth_exception()
    return (
        db.query(Todos)
        .filter(Todos.user_id == user.get("id"))
        .all()
    )


@router.get("/{todo_id}/")
async def read_todo(
    todo_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    if user is None:
        raise get_auth_exception()
    todo_instance = (
        db.query(Todos)
        .filter(Todos.user_id == user.get("id"))
        .filter(Todos.id == todo_id)
        .first()
    )
    if not todo_instance:
        raise http_exception()
    return todo_instance


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_data: TodoSchema,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    if user is None:
        raise get_auth_exception()
    todo = Todos()
    todo.title = todo_data.title
    todo.description = todo_data.description
    todo.priority = todo_data.priority
    todo.completed = todo_data.completed
    todo.user_id = user.get("id")
    db.add(todo)
    db.commit()
    return successful_response(201)


@router.put("/{todo_id}/")
async def update_todo(
    todo_id: int,
    todo_data: TodoSchema,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    if user is None:
        raise get_auth_exception()
    todo_instance = (
        db.query(Todos)
        .filter(Todos.user_id == user.get("id"))
        .filter(Todos.id == todo_id)
        .first()
    )
    if not todo_instance:
        raise http_exception()
    todo_instance.title = todo_data.title
    todo_instance.description = todo_data.description
    todo_instance.priority = todo_data.priority
    todo_instance.completed = todo_data.completed
    db.add(todo_instance)
    db.commit()
    return successful_response(200)


@router.delete("/{todo_id}/")
async def delete_todo(
    todo_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> str:
    if user is None:
        raise get_auth_exception()
    todo_instance = (
        db.query(Todos)
        .filter(Todos.user_id == user.get("id"))
        .filter(Todos.id == todo_id)
        .first()
    )
    if not todo_instance:
        raise http_exception()
    db.query(Todos).filter(Todos.id == todo_id).filter(
        Todos.user_id == user.get("id")
    ).delete()
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
                "msg": "Todo not found",
                "type": "string",
            }
        ],
    )
