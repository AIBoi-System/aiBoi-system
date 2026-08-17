from sqlalchemy import and_, exists, or_
from sqlalchemy.orm import Session

from app.shared.infrastructure.persistence.address import Address
from app.shared.infrastructure.persistence.property import Property
from app.shared.infrastructure.persistence.user import User


def create_address(db: Session, address_data: dict):
    new_address = Address(**address_data)
    try:
        db.add(new_address)
        db.commit()
        db.refresh(new_address)
    except Exception:
        db.rollback()
        raise
    return new_address


def get_address_by_id(
    db: Session, address_id: int, owner_id: int | None = None
):
    query = db.query(Address).filter(Address.id_address == address_id)
    if owner_id is not None:
        user_link = exists().where(
            and_(
                User.id_user == owner_id,
                User.address_id == Address.id_address,
            )
        )
        property_link = exists().where(
            and_(
                Property.owner_id == owner_id,
                Property.address_id == Address.id_address,
            )
        )
        query = query.filter(or_(user_link, property_link))
    return query.first()


def get_all_addresses(db: Session):
    return db.query(Address).all()


def is_address_assignable_to_owner(
    db: Session,
    address_id: int,
    owner_id: int,
    exclude_property_id: int | None = None,
) -> bool:
    if not db.query(Address.id_address).filter(Address.id_address == address_id).first():
        return False

    conflicting_user = (
        db.query(User.id_user)
        .filter(User.address_id == address_id, User.id_user != owner_id)
        .first()
    )
    property_query = db.query(Property.id_property).filter(
        Property.address_id == address_id,
        Property.owner_id != owner_id,
    )
    if exclude_property_id is not None:
        property_query = property_query.filter(
            Property.id_property != exclude_property_id
        )
    return conflicting_user is None and property_query.first() is None


def update_address(
    db: Session,
    address_id: int,
    data: dict,
    owner_id: int | None = None,
):
    db_address = get_address_by_id(db, address_id, owner_id=owner_id)
    if not db_address:
        return None
    for key, value in data.items():
        setattr(db_address, key, value)
    try:
        db.commit()
        db.refresh(db_address)
    except Exception:
        db.rollback()
        raise
    return db_address


def delete_address(db: Session, address_id: int):
    db_address = get_address_by_id(db, address_id)
    if not db_address:
        return None
    try:
        db.delete(db_address)
        db.commit()
    except Exception:
        db.rollback()
        raise
    return db_address
