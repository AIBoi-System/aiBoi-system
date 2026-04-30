from fastapi import HTTPException, status
from passlib.context import CryptContext

from repositories.owner_repository import (
    create_owner,
    get_owner_by_id,
    get_owner_by_email,
    get_all_owners,
    update_owner,
    delete_owner,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def create_owner_service(db, owner_data):
    existing_email = get_owner_by_email(db, owner_data.email)

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado."
        )

    owners = get_all_owners(db)

    for owner in owners:
        if owner.cpf == owner_data.cpf:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CPF já cadastrado."
            )

    data = owner_data.model_dump()
    data["password"] = hash_password(data["password"])
    data["subscription_status"] = "inactive"

    return create_owner(db, data)


def get_owner_service(db, id_user: int):
    owner = get_owner_by_id(db, id_user)

    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Owner não encontrado."
        )

    return owner


def list_owners_service(db):
    return get_all_owners(db)


def update_owner_service(db, id_user: int, owner_data):
    owner = get_owner_by_id(db, id_user)

    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Owner não encontrado."
        )

    data = owner_data.model_dump(exclude_unset=True)

    if "email" in data:
        existing_email = get_owner_by_email(db, data["email"])

        if existing_email and existing_email.id_user != id_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado."
            )

    if "password" in data:
        data["password"] = hash_password(data["password"])

    return update_owner(db, id_user, data)


def delete_owner_service(db, id_user: int):
    owner = get_owner_by_id(db, id_user)

    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Owner não encontrado."
        )

    if owner.properties and len(owner.properties) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível excluir Owner com propriedades vinculadas."
        )

    return delete_owner(db, id_user)