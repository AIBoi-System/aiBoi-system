from fastapi import HTTPException
from app.infrastructure.persistence.repositories.weighing_repository import WeighingRepository
from app.infrastructure.persistence.models.animal import AnimalModel
from sqlalchemy.orm import Session

class WeighingService:
    @staticmethod
    def create_weighing(db, payload):
        # Validação fica no Service
        animal = db.query(AnimalModel).filter(AnimalModel.id_animal == payload.animal_id).first()
        if not animal:
            raise HTTPException(status_code=404, detail="Animal não encontrado")
        
        # O banco é chamado via Repository
        return WeighingRepository.create(db, payload.model_dump())

    @staticmethod
    def get_history_by_animal(db, animal_id: int):
        return WeighingRepository.get_by_animal(db, animal_id)

    @staticmethod
    def update_weighing(db, weighing_id: int, payload):
        db_weighing = WeighingRepository.get_by_id(db, weighing_id)
        if not db_weighing:
            raise HTTPException(status_code=404, detail="Pesagem não encontrada")
            
        update_data = payload.model_dump(exclude_unset=True)
        return WeighingRepository.update(db, db_weighing, update_data)
    
    @staticmethod
    def delete_weighing(db: Session, weighing_id: int):
        db_weighing = WeighingRepository.get_by_id(db, weighing_id)
        if not db_weighing:
            raise HTTPException(status_code=404, detail="Weighing not found")
        return WeighingRepository.delete(db, db_weighing)
