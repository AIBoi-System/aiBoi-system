from sqlalchemy.orm import Session

from app.modules.inventory.infrastructure.persistence.animal import AnimalModel
from app.modules.inventory.infrastructure.persistence.weighing import Weighing


class WeighingRepository:
    @staticmethod
    def get_by_id(db: Session, weighing_id: int, property_id: int):
        return (
            db.query(Weighing)
            .join(AnimalModel, Weighing.animal_id == AnimalModel.id_animal)
            .filter(Weighing.id == weighing_id, AnimalModel.property_id == property_id)
            .first()
        )

    @staticmethod
    def get_by_animal(db: Session, animal_id: int, property_id: int):
        return (
            db.query(Weighing)
            .join(AnimalModel, Weighing.animal_id == AnimalModel.id_animal)
            .filter(
                Weighing.animal_id == animal_id,
                AnimalModel.property_id == property_id,
            )
            .all()
        )

    @staticmethod
    def create(db: Session, weighing_data: dict):
        db_weighing = Weighing(**weighing_data)
        try:
            db.add(db_weighing)
            db.commit()
            db.refresh(db_weighing)
        except Exception:
            db.rollback()
            raise
        return db_weighing

    @staticmethod
    def update(db: Session, db_weighing: Weighing, update_data: dict):
        for key, value in update_data.items():
            setattr(db_weighing, key, value)
        try:
            db.commit()
            db.refresh(db_weighing)
        except Exception:
            db.rollback()
            raise
        return db_weighing

    @staticmethod
    def delete(db: Session, db_weighing: Weighing):
        try:
            db.delete(db_weighing)
            db.commit()
        except Exception:
            db.rollback()
            raise
        return True
