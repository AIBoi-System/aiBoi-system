from fastapi import HTTPException, status
from passlib.context import CryptContext

# importa validações do User (pois email e CPF são únicos para todos)
from app.infrastructure.persistence.repositories.user_repository import (
    get_user_by_email,
    get_user_by_cpf,
)

from app.infrastructure.persistence.repositories.owner_repository import (
    create_owner,
    get_owner_by_id,
    get_all_owners,
    update_owner,
    delete_owner,
    upgrade_user_to_owner,  # importado para suportar o upgrade
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def create_owner_service(db, owner_data):
    #  validações nas regras de Usuário
    if get_user_by_email(db, owner_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado."
        )

    if get_user_by_cpf(db, owner_data.cpf):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="CPF já cadastrado."
        )

    data = owner_data.model_dump()
    data["password"] = hash_password(data["password"])

    # como a  classe owner herda de user, passa o dicionario
    # inteiro de uma vez. o SQLAlchemy salva nas duas tabelas automaticamente.
    return create_owner(db, data)


def get_owner_service(db, id_user: int):
    owner = get_owner_by_id(db, id_user)
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Owner não encontrado."
        )
    return owner


def list_owners_service(db):
    return get_all_owners(db)


def update_owner_service(db, id_user: int, owner_data):
    owner = get_owner_by_id(db, id_user)
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Owner não encontrado."
        )

    data = owner_data.model_dump(exclude_unset=True)

    if "email" in data:
        existing_email = get_user_by_email(db, data["email"])
        if existing_email and existing_email.id_user != id_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado."
            )

    if "password" in data:
        data["password"] = hash_password(data["password"])

    #  o update também funciona direto, o SQLAlchemy sabe o que
    # atualizar em users e o que atualizar em owners
    return update_owner(db, id_user, data)


def delete_owner_service(db, id_user: int):
    owner = get_owner_by_id(db, id_user)
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Owner não encontrado."
        )

    if owner.properties and len(owner.properties) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível excluir Owner com propriedades vinculadas.",
        )

    #  ao deletar o objeto polimórfico, o SQLAlchemy cuida da exclusão
    delete_owner(db, id_user)

    return {"detail": "Owner deletado com sucesso."}


#  Faz a ponte entre o Controller e o Repositorio com trava de segurança
def upgrade_user_to_owner_service(db, id_user: int, subscription_status: str):
    # 1. Verifica se o cara já é dono. Se for, nem tenta
    if get_owner_by_id(db, id_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este usuário já é um proprietário (Owner).",
        )

    # 2. Se não for dono, chama o repositório
    owner = upgrade_user_to_owner(db, id_user, subscription_status)

    # 3. Se o repositório retornar none, é porque o ID do usuário não existe
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado para realizar o upgrade.",
        )

    return owner

