from sqlalchemy.orm import Session

from app.presentation.schemas.pasture_schema import PastureCreate, PastureUpdate
from app.shared.infrastructure.persistence.pasture import Pasture


class PastureRepository:
    def get_all(
        self, db: Session, property_id: int, skip: int = 0, limit: int = 100
    ):
        return (
            db.query(Pasture)
            .filter(Pasture.property_id == property_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, db: Session, pasture_id: int, property_id: int):
        return (
            db.query(Pasture)
            .filter(
                Pasture.id_pasture == pasture_id,
                Pasture.property_id == property_id,
            )
            .first()
        )

    def create(self, db: Session, pasture: PastureCreate):
        db_pasture = Pasture(**pasture.model_dump())
        try:
            db.add(db_pasture)
            db.commit()
            db.refresh(db_pasture)
        except Exception:
            db.rollback()
            raise
        return db_pasture

    def update(
        self, db: Session, pasture_id: int, property_id: int, pasture_update: PastureUpdate
    ):
        db_pasture = self.get_by_id(db, pasture_id, property_id)
        if db_pasture is None:
            return None

        update_data = pasture_update.model_dump(exclude_unset=True)
        update_data.pop("property_id", None)
        for key, value in update_data.items():
            setattr(db_pasture, key, value)

        try:
            db.commit()
            db.refresh(db_pasture)
        except Exception:
            db.rollback()
            raise
        return db_pasture

    def delete(self, db: Session, pasture_id: int, property_id: int):
        db_pasture = self.get_by_id(db, pasture_id, property_id)
        if db_pasture is None:
            return None
        try:
            db.delete(db_pasture)
            db.commit()
        except Exception:
            db.rollback()
            raise
        return db_pasture


pasture_repository = PastureRepository()
