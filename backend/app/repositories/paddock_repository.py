from sqlalchemy.orm import Session
from app.models.paddock import Paddock
from app.schemas.paddock_schema import PaddockCreate, PaddockUpdate


class PaddockRepository:
    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        property_id: int = None,
        pasture_id: int = None,
    ):
        query = db.query(Paddock)

        # filtros para a busca
        if property_id:
            query = query.filter(Paddock.property_id == property_id)
        if pasture_id:
            query = query.filter(Paddock.pasture_id == pasture_id)

        return query.offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, paddock_id: int):
        return db.query(Paddock).filter(Paddock.id_paddock == paddock_id).first()

    def create(self, db: Session, paddock: PaddockCreate):
        db_paddock = Paddock(**paddock.model_dump())
        db.add(db_paddock)
        db.commit()
        db.refresh(db_paddock)
        return db_paddock

    def update(self, db: Session, db_paddock: Paddock, paddock_update: PaddockUpdate):
        update_data = paddock_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_paddock, key, value)

        db.commit()
        db.refresh(db_paddock)
        return db_paddock

    def delete(self, db: Session, db_paddock: Paddock):
        db.delete(db_paddock)
        db.commit()
        return db_paddock


# instancia unica
paddock_repository = PaddockRepository()
