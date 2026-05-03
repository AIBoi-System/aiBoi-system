from sqlalchemy.orm import Session
from app.models.property import Property


class PropertyRepository:

    @staticmethod
    def create(db: Session, property_data: Property) -> Property:
        db.add(property_data)
        db.commit()
        db.refresh(property_data)
        return property_data

    @staticmethod
    def get_by_id(db: Session, property_id: int) -> Property:
        return db.query(Property).filter(Property.id_property == property_id).first()

    @staticmethod
    def get_all(db: Session) -> list[Property]:
        return db.query(Property).all()

    @staticmethod
    def update(db: Session, property_db: Property) -> Property:
        db.commit()
        db.refresh(property_db)
        return property_db

    @staticmethod
    def delete(db: Session, property_db: Property):
        db.delete(property_db)
        db.commit()
