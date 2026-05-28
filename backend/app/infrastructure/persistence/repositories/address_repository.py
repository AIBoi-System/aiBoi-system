from sqlalchemy.orm import Session
from app.infrastructure.persistence.models.address import Address


def create_address(db: Session, address_data: dict):
    new_address = Address(**address_data)
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address


def get_address_by_id(db: Session, address_id: int):
    return db.query(Address).filter(Address.id_address == address_id).first()


def get_all_addresses(db: Session):
    return db.query(Address).all()


def update_address(db: Session, address_id: int, data: dict):
    db_address = get_address_by_id(db, address_id)
    if not db_address:
        return None
    for key, value in data.items():
        setattr(db_address, key, value)
    db.commit()
    db.refresh(db_address)
    return db_address


def delete_address(db: Session, address_id: int):
    db_address = get_address_by_id(db, address_id)
    if not db_address:
        return None
    db.delete(db_address)
    db.commit()
    return db_address

