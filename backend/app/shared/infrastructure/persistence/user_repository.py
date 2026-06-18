from sqlalchemy.orm import Session
from app.shared.infrastructure.persistence.user import User


def create_user(db: Session, user_data: dict):
    """
    Cria um usuário no banco de dados.
    user_data: dicionário já validado e formatado pelo Service.
    """
    # Como o Service já envia um dicionário pronto, 
    # apenas desempacotamos ele no Model User
    user = User(**user_data)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_cpf(db: Session, cpf: str):
    return db.query(User).filter(User.cpf == cpf).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id_user == user_id).first()


def get_all_users(db: Session):
    return db.query(User).all()


def update_user(db: Session, user_id: int, user_data: dict):
    """
    Atualiza um usuário.
    user_data: dicionário com os campos que devem ser alterados.
    """
    user = get_user_by_id(db, user_id)

    if not user:
        return None

    # Itera sobre o dicionário já tratado pelo Service
    for key, value in user_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)

    if user:
        db.delete(user)
        db.commit()










































