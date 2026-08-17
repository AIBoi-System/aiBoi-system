from sqlalchemy.orm import Session

from app.shared.infrastructure.persistence.property import Property


class PropertyRepository:
    @staticmethod
    def create(db: Session, property_data: Property) -> Property:
        try:
            db.add(property_data)
            db.commit()
            db.refresh(property_data)
        except Exception:
            db.rollback()
            raise
        return property_data

    @staticmethod
    def get_by_id(
        db: Session, property_id: int, owner_id: int | None = None
    ) -> Property | None:
        query = db.query(Property).filter(Property.id_property == property_id)
        if owner_id is not None:
            query = query.filter(Property.owner_id == owner_id)
        return query.first()

    @staticmethod
    def get_all(db: Session, owner_id: int | None = None) -> list[Property]:
        query = db.query(Property)
        if owner_id is not None:
            query = query.filter(Property.owner_id == owner_id)
        return query.all()

    @staticmethod
    def update(db: Session, property_db: Property) -> Property:
        try:
            db.commit()
            db.refresh(property_db)
        except Exception:
            db.rollback()
            raise
        return property_db

    @staticmethod
    def delete(db: Session, property_db: Property):
        try:
            db.delete(property_db)
            db.commit()
        except Exception:
            db.rollback()
            raise
