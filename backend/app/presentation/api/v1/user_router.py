from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.shared.application.user.user_service as user_service
from app.shared.infrastructure.database.connection import get_db
from app.presentation.schemas.user import (
    UserCreateSchema,
    UserResponseSchema,
    UserUpdateSchema,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponseSchema)
def create_user(
    data: UserCreateSchema,
    db: Session = Depends(get_db),
):
    return user_service.create_user_service(db, data)


@router.get("/", response_model=list[UserResponseSchema])
def list_users(
    db: Session = Depends(get_db),
):
    return user_service.list_users_service(db)


@router.get("/{user_id}", response_model=UserResponseSchema)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    return user_service.get_user_service(db, user_id)


@router.put("/{user_id}", response_model=UserResponseSchema)
def update_user(
    user_id: int,
    data: UserUpdateSchema,
    db: Session = Depends(get_db),
):
    return user_service.update_user_service(db, user_id, data)


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user_service.delete_user_service(db, user_id)
    return {"message": "Usuário deletado com sucesso"}














































