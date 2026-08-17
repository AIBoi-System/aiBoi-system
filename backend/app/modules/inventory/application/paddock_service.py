from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.presentation.schemas.paddock_schema import PaddockCreate, PaddockUpdate
from app.shared.infrastructure.persistence.paddock_repository import paddock_repository
from app.shared.infrastructure.persistence.pasture_repository import pasture_repository
from app.shared.infrastructure.persistence.property_repository import PropertyRepository


class PaddockService:
    def create_paddock(self, db: Session, paddock: PaddockCreate):
        if not PropertyRepository.get_by_id(db, paddock.property_id):
            raise HTTPException(status_code=404, detail="Property not found")

        if paddock.pasture_id is not None and not pasture_repository.get_by_id(
            db, paddock.pasture_id, paddock.property_id
        ):
            raise HTTPException(status_code=404, detail="Pasture not found")
        return paddock_repository.create(db, paddock)

    def get_paddocks(
        self,
        db: Session,
        property_id: int,
        skip: int = 0,
        limit: int = 100,
        pasture_id: int | None = None,
    ):
        return paddock_repository.get_all(
            db,
            property_id=property_id,
            skip=skip,
            limit=limit,
            pasture_id=pasture_id,
        )

    def get_paddock(self, db: Session, paddock_id: int, property_id: int):
        db_paddock = paddock_repository.get_by_id(db, paddock_id, property_id)
        if not db_paddock:
            raise HTTPException(status_code=404, detail="Paddock not found")
        return db_paddock

    def update_paddock(
        self,
        db: Session,
        paddock_id: int,
        property_id: int,
        paddock_update: PaddockUpdate,
    ):
        self.get_paddock(db, paddock_id, property_id)
        requested_property_id = getattr(paddock_update, "property_id", None)
        if requested_property_id is not None and requested_property_id != property_id:
            raise HTTPException(
                status_code=400,
                detail="Moving a paddock between properties is not allowed.",
            )
        requested_pasture_id = getattr(paddock_update, "pasture_id", None)
        if requested_pasture_id is not None and not pasture_repository.get_by_id(
            db, requested_pasture_id, property_id
        ):
            raise HTTPException(status_code=404, detail="Pasture not found")
        return paddock_repository.update(
            db, paddock_id, property_id, paddock_update
        )

    def delete_paddock(self, db: Session, paddock_id: int, property_id: int):
        self.get_paddock(db, paddock_id, property_id)
        return paddock_repository.delete(db, paddock_id, property_id)


paddock_service = PaddockService()
