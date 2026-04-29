from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.schemas.user import (
    UserCreateSchema,
    UserUpdateSchema,
    UserResponseSchema
)
from app.services.user_service import (
    create_user_service,
    get_user_service,
    list_users_service,
    update_user_service,
    delete_user_service
)

router = APIRouter(prefix="/users", tags=["Users"])


# 🔌 conexão com banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/", response_model=UserResponseSchema)
def create_user(data: UserCreateSchema, db: Session = Depends(get_db)):
    return create_user_service(db, data)



@router.get("/", response_model=list[UserResponseSchema])
def list_users(db: Session = Depends(get_db)):
    return list_users_service(db)



@router.get("/{user_id}", response_model=UserResponseSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_service(db, user_id)



@router.put("/{user_id}", response_model=UserResponseSchema)
def update_user(user_id: int, data: UserUpdateSchema, db: Session = Depends(get_db)):
    return update_user_service(db, user_id, data)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    delete_user_service(db, user_id)
    return {"message": "Usuário deletado com sucesso"}