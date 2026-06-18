from sqlalchemy.orm import Session
from app.shared.infrastructure.persistence.pasture import Pasture
from app.presentation.schemas.pasture_schema import PastureCreate, PastureUpdate


class PastureRepository:
    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, property_id: int = None
    ):
        query = db.query(Pasture)
        # Filtra pela fazenda específica, se o id for passado
        if property_id:
            query = query.filter(Pasture.property_id == property_id)
        return query.offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, pasture_id: int):
        return db.query(Pasture).filter(Pasture.id_pasture == pasture_id).first()

    def create(self, db: Session, pasture: PastureCreate):

        db_pasture = Pasture(**pasture.model_dump())
        db.add(db_pasture)
        db.commit()
        db.refresh(db_pasture)
        return db_pasture

    def update(self, db: Session, db_pasture: Pasture, pasture_update: PastureUpdate):
        # exclude_unset=True garante que só atualiza os campos que o usuário realmente enviou
        update_data = pasture_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_pasture, key, value)

        db.commit()
        db.refresh(db_pasture)
        return db_pasture

    def delete(self, db: Session, db_pasture: Pasture):
        db.delete(db_pasture)
        db.commit()
        return db_pasture


# instancia única
pasture_repository = PastureRepository()











































