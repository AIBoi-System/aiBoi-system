from sqlalchemy.orm import Session

from app.presentation.schemas.paddock_schema import PaddockCreate, PaddockUpdate
from app.shared.infrastructure.persistence.paddock import Paddock


class PaddockRepository:
    def get_all(
        self,
        db: Session,
        property_id: int,
        skip: int = 0,
        limit: int = 100,
        pasture_id: int | None = None,
    ):
        query = db.query(Paddock).filter(Paddock.property_id == property_id)
        if pasture_id is not None:
            query = query.filter(Paddock.pasture_id == pasture_id)
        return query.offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, paddock_id: int, property_id: int):
        return (
            db.query(Paddock)
            .filter(
                Paddock.id_paddock == paddock_id,
                Paddock.property_id == property_id,
            )
            .first()
        )

    def create(self, db: Session, paddock: PaddockCreate):
        db_paddock = Paddock(**paddock.model_dump())
        try:
            db.add(db_paddock)
            db.commit()
            db.refresh(db_paddock)
        except Exception:
            db.rollback()
            raise
        return db_paddock

    def update(
        self, db: Session, paddock_id: int, property_id: int, paddock_update: PaddockUpdate
    ):
        db_paddock = self.get_by_id(db, paddock_id, property_id)
        if db_paddock is None:
            return None

        update_data = paddock_update.model_dump(exclude_unset=True)
        update_data.pop("property_id", None)
        for key, value in update_data.items():
            setattr(db_paddock, key, value)

        try:
            db.commit()
            db.refresh(db_paddock)
        except Exception:
            db.rollback()
            raise
        return db_paddock

    def delete(self, db: Session, paddock_id: int, property_id: int):
        db_paddock = self.get_by_id(db, paddock_id, property_id)
        if db_paddock is None:
            return None
        try:
            db.delete(db_paddock)
            db.commit()
        except Exception:
            db.rollback()
            raise
        return db_paddock


paddock_repository = PaddockRepository()
