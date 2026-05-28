from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.infrastructure.persistence.models.batch import Batch


class BatchService:
    @staticmethod
    def create_batch(db: Session, data):
        batch = Batch(**data.model_dump())
        db.add(batch)
        db.commit()
        db.refresh(batch)
        return batch

    @staticmethod
    def list_batches(db: Session):
        return db.query(Batch).all()

    @staticmethod
    def get_batch(db: Session, batch_id: int):
        batch = db.query(Batch).filter(Batch.id_batch == batch_id).first()
        if not batch:
            raise HTTPException(status_code=404, detail="Batch não encontrado.")
        return batch

    @staticmethod
    def update_batch(db: Session, batch_id: int, data):
        batch = BatchService.get_batch(db, batch_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(batch, key, value)
        db.commit()
        db.refresh(batch)
        return batch

    @staticmethod
    def delete_batch(db: Session, batch_id: int):
        batch = BatchService.get_batch(db, batch_id)
        db.delete(batch)
        db.commit()
