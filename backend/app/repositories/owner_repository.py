from sqlalchemy.orm import Session

from models.owner import Owner


def create_owner(db: Session, owner_data):
    owner = Owner(**owner_data)

    db.add(owner)
    db.commit()
    db.refresh(owner)

    return owner


def get_owner_by_id(db: Session, id_user: int):
    return db.query(Owner).filter(Owner.id_user == id_user).first()


def get_owner_by_email(db: Session, email: str):
    return db.query(Owner).filter(Owner.email == email).first()


def get_all_owners(db: Session):
    return db.query(Owner).all()


def update_owner(db: Session, id_user: int, data):
    owner = get_owner_by_id(db, id_user)

    if owner is None:
        return None

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