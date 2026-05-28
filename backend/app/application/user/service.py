from fastapi import HTTPException
from sqlalchemy.orm import Session
import logging

from app.infrastructure.persistence.repositories.user_repository import (
    create_user,
    get_user_by_email,
    get_user_by_cpf,
    get_user_by_id,
    get_all_users,
    update_user,
    delete_user
)

from app.infrastructure.security import hash_password
from app.infrastructure.persistence.models.cpf import CPF  

# 1. FUNÇÃO DE CRIAR
def create_user_service(db: Session, data):
    # 1. Validar email único
    if get_user_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # 2. VALIDAR E FORMATAR CPF
    try:
        # Limpamos e validamos usando sua classe CPF
        cpf_limpo = "".join(filter(str.isdigit, str(data.cpf)))
        cpf_objeto = CPF(cpf_limpo)
        
        # Guardamos o valor formatado (com pontos e traço)
        cpf_formatado = str(cpf_objeto)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Erro na classe CPF: {str(e)}")

    # 3. Validar se o CPF formatado já existe no banco
    if get_user_by_cpf(db, cpf_formatado):
        raise HTTPException(status_code=400, detail="CPF já cadastrado")

    # 4. PREPARAR DICIONÁRIO (Ajustado para o seu banco)
    # Transformamos o Schema em dicionário para manipular os campos
    user_dict = data.dict()
    
    # Forçamos os valores que foram tratados no Service
    user_dict["cpf"] = cpf_formatado
    user_dict["password"] = hash_password(data.password)
    
    # Adicionamos o campo 'type' que vimos na sua imagem do MySQL
    # Isso evita erros de "campo obrigatório" no banco
    if "type" not in user_dict:
        user_dict["type"] = "user" 

    # 5. Enviamos o DICIONÁRIO para o repository
    return create_user(db, user_dict)


# 2. FUNÇÃO DE LISTAR
def list_users_service(db: Session):
    return get_all_users(db)


# 3. FUNÇÃO DE BUSCAR UM
def get_user_service(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


# 4. FUNÇÃO DE ATUALIZAR
def update_user_service(db: Session, user_id: int, data):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # 1. Transforma o Schema de Update em dicionário (apenas o que foi enviado)
    update_data = data.dict(exclude_unset=True)

    # 2. Se o CPF estiver sendo atualizado, validamos e formatamos
    if "cpf" in update_data:
        try:
            cpf_limpo = "".join(filter(str.isdigit, str(update_data["cpf"])))
            update_data["cpf"] = str(CPF(cpf_limpo))
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"CPF inválido: {str(e)}")

    # 3. Se a senha estiver sendo atualizada, fazemos o hash
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    # 4. Passamos o dicionário para o repositório
    return update_user(db, user_id, update_data)


# 5. FUNÇÃO DE DELETAR
def delete_user_service(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return delete_user(db, user_id)
