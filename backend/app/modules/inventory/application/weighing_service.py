from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.inventory.infrastructure.persistence.animal import AnimalModel
from app.shared.infrastructure.persistence.weighing_repository import WeighingRepository


class WeighingService:
    @staticmethod
    def _get_animal(db: Session, animal_id: int, property_id: int):
        animal = (
            db.query(AnimalModel)
            .filter(
                AnimalModel.id_animal == animal_id,
                AnimalModel.property_id == property_id,
            )
            .first()
        )
        if not animal:
            raise HTTPException(status_code=404, detail="Animal not found")
        return animal

    @staticmethod
    def create_weighing(db: Session, payload, property_id: int):
        WeighingService._get_animal(db, payload.animal_id, property_id)
        return WeighingRepository.create(db, payload.model_dump())

    @staticmethod
    def get_history_by_animal(db: Session, animal_id: int, property_id: int):
        WeighingService._get_animal(db, animal_id, property_id)
        return WeighingRepository.get_by_animal(db, animal_id, property_id)

    @staticmethod
    def update_weighing(db: Session, weighing_id: int, property_id: int, payload):
        db_weighing = WeighingRepository.get_by_id(db, weighing_id, property_id)
        if not db_weighing:
            raise HTTPException(status_code=404, detail="Weighing not found")

        update_data = payload.model_dump(exclude_unset=True)
        new_animal_id = update_data.get("animal_id")
        if new_animal_id is not None:
            WeighingService._get_animal(db, new_animal_id, property_id)
        return WeighingRepository.update(db, db_weighing, update_data)

    @staticmethod
    def delete_weighing(db: Session, weighing_id: int, property_id: int):
        db_weighing = WeighingRepository.get_by_id(db, weighing_id, property_id)
        if not db_weighing:
            raise HTTPException(status_code=404, detail="Weighing not found")
        return WeighingRepository.delete(db, db_weighing)
