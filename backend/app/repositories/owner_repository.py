from sqlalchemy.orm import Session
from sqlalchemy import update, insert

# adicionando o .app
from app.models.user import User  # precisamos do modelo User para a promoção
from app.models.owner import Owner
from app.models.address import Address  # Importamos o modelo de endereço


def create_owner(db: Session, owner_data: dict):
    # Tiramos o endereço do dicionário antes de criar o Owner
    address_data = owner_data.pop("address", None)

    # Criamos o dono no SQLAlchemy
    owner = Owner(**owner_data)

    # Se veio um endereço no JSON, transformamos ele em modelo e associa ao dono
    if address_data:
        owner.address = Address(**address_data)

    db.add(owner)
    db.commit()
    db.refresh(owner)

    return owner


def get_owner_by_id(db: Session, id_user: int):
    return db.query(Owner).filter(Owner.id_user == id_user).first()


def get_all_owners(db: Session):
    return db.query(Owner).all()


def update_owner(db: Session, id_user: int, data: dict):
    owner = get_owner_by_id(db, id_user)

    if owner is None:
        return None

    # trata o endereço no update também
    address_data = data.pop("address", None)
    if address_data:
        if owner.address:
            # se ele já tem endereço, atualiza os campos
            for key, value in address_data.items():
                setattr(owner.address, key, value)
        else:
            # se não tinha, cria um novo
            owner.address = Address(**address_data)

    # atualiza o restante dos campos normais (nome, cpf, assinatura, etc)
    for field, value in data.items():
        setattr(owner, field, value)

    db.commit()
    db.refresh(owner)

    return owner


def delete_owner(db: Session, id_user: int):
    owner = get_owner_by_id(db, id_user)

    if owner is None:
        return None

    db.delete(owner)
    db.commit()

    return owner


def upgrade_user_to_owner(db: Session, id_user: int, subscription_status: str = "FREE"):
    # 1. Verifica se o usuário existe na tabela base (User)
    user = db.query(User).filter(User.id_user == id_user).first()
    if not user:
        return None

    # 2. Verifica se ele já possui um registro na tabela Owner
    existing_owner = db.query(Owner).filter(Owner.id_owner == id_user).first()

    # 3. Garante que o 'type' na tabela users seja 'owner' (Polimorfismo)
    db.execute(update(User).where(User.id_user == id_user).values(type="owner"))

    if not existing_owner:
        # Se não existe na tabela owners, fazemos o INSERT
        db.execute(
            insert(Owner).values(
                id_owner=id_user, subscription_status=subscription_status
            )
        )
    else:
        # Se já existe, fazemos apenas um UPDATE
        db.execute(
            update(Owner)
            .where(Owner.id_owner == id_user)
            .values(subscription_status=subscription_status)
        )

    db.commit()

    # Expira os objetos da sessão para forçar o reload e o SQLAlchemy
    # entender que o objeto mudou de User para Owner
    db.expire_all()

    # Agora o get_owner_by_id buscará o objeto Owner atualizado
    return get_owner_by_id(db, id_user)
