from sqlalchemy.orm import Session
from app.modules.inventory.infrastructure.persistence.weighing import Weighing

class WeighingRepository:
    @staticmethod
    def get_by_id(db: Session, weighing_id: int):
        return db.query(Weighing).filter(Weighing.id == weighing_id).first()

    @staticmethod
    def get_by_animal(db: Session, animal_id: int):
        return db.query(Weighing).filter(Weighing.animal_id == animal_id).all()

    @staticmethod
    def create(db: Session, weighing_data: dict):
        db_weighing = Weighing(**weighing_data)
        db.add(db_weighing)
        db.commit()
        db.refresh(db_weighing)
        return db_weighing

    @staticmethod
    def update(db: Session, db_weighing: Weighing, update_data: dict):
        for key, value in update_data.items():
            setattr(db_weighing, key, value)
        db.commit()
        db.refresh(db_weighing)
        return db_weighing
    
    @staticmethod
    def delete(db: Session, db_weighing: Weighing):
        db.delete(db_weighing)
        db.commit()
        return True










































