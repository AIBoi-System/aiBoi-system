from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.presentation.schemas.pasture_schema import PastureCreate, PastureUpdate
from app.shared.infrastructure.persistence.pasture_repository import pasture_repository
from app.shared.infrastructure.persistence.property_repository import PropertyRepository


class PastureService:
    def create_pasture(self, db: Session, pasture: PastureCreate):
        if not PropertyRepository.get_by_id(db, pasture.property_id):
            raise HTTPException(status_code=404, detail="Property not found")
        return pasture_repository.create(db, pasture)

    def get_pastures(
        self, db: Session, property_id: int, skip: int = 0, limit: int = 100
    ):
        return pasture_repository.get_all(
            db, property_id=property_id, skip=skip, limit=limit
        )

    def get_pasture(self, db: Session, pasture_id: int, property_id: int):
        db_pasture = pasture_repository.get_by_id(db, pasture_id, property_id)
        if not db_pasture:
            raise HTTPException(status_code=404, detail="Pasture not found")
        return db_pasture

    def update_pasture(
        self,
        db: Session,
        pasture_id: int,
        property_id: int,
        pasture_update: PastureUpdate,
    ):
        self.get_pasture(db, pasture_id, property_id)
        requested_property_id = getattr(pasture_update, "property_id", None)
        if requested_property_id is not None and requested_property_id != property_id:
            raise HTTPException(
                status_code=400,
                detail="Moving a pasture between properties is not allowed.",
            )
        return pasture_repository.update(
            db, pasture_id, property_id, pasture_update
        )

    def delete_pasture(self, db: Session, pasture_id: int, property_id: int):
        self.get_pasture(db, pasture_id, property_id)
        return pasture_repository.delete(db, pasture_id, property_id)


pasture_service = PastureService()
