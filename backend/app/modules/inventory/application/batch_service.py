from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.inventory.infrastructure.persistence.batch import Batch
from app.shared.infrastructure.persistence.property_repository import PropertyRepository


class BatchService:
    @staticmethod
    def create_batch(db: Session, data):
        if not PropertyRepository.get_by_id(db, data.property_id):
            raise HTTPException(status_code=404, detail="Property not found.")

        batch = Batch(**data.model_dump())
        try:
            db.add(batch)
            db.commit()
            db.refresh(batch)
        except Exception:
            db.rollback()
            raise
        return batch

    @staticmethod
    def list_batches(db: Session, property_id: int):
        return db.query(Batch).filter(Batch.property_id == property_id).all()

    @staticmethod
    def get_batch(db: Session, batch_id: int, property_id: int):
        batch = (
            db.query(Batch)
            .filter(Batch.id_batch == batch_id, Batch.property_id == property_id)
            .first()
        )
        if not batch:
            raise HTTPException(status_code=404, detail="Batch not found.")
        return batch

    @staticmethod
    def update_batch(db: Session, batch_id: int, property_id: int, data):
        batch = BatchService.get_batch(db, batch_id, property_id)
        new_property_id = getattr(data, "property_id", None)
        if new_property_id is not None and new_property_id != property_id:
            raise HTTPException(
                status_code=400,
                detail="Moving a batch between properties is not allowed.",
            )

        update_data = data.model_dump(exclude_unset=True)
        update_data.pop("property_id", None)
        for key, value in update_data.items():
            setattr(batch, key, value)
        try:
            db.commit()
            db.refresh(batch)
        except Exception:
            db.rollback()
            raise
        return batch

    @staticmethod
    def delete_batch(db: Session, batch_id: int, property_id: int):
        batch = BatchService.get_batch(db, batch_id, property_id)
        try:
            db.delete(batch)
            db.commit()
        except Exception:
            db.rollback()
            raise
