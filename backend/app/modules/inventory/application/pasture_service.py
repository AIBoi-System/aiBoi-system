from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.shared.infrastructure.persistence.pasture_repository import pasture_repository
from app.shared.infrastructure.persistence.property_repository import PropertyRepository
from app.presentation.schemas.pasture_schema import PastureCreate, PastureUpdate


class PastureService:
    def create_pasture(self, db: Session, pasture: PastureCreate):
        # regra de negócio: a propriedade existe?
        db_property = PropertyRepository.get_by_id(db, pasture.property_id)
        if not db_property:
            raise HTTPException(status_code=404, detail="Property not found")

        # se passou pela validação, manda criar
        return pasture_repository.create(db, pasture)

    def get_pastures(
        self, db: Session, skip: int = 0, limit: int = 100, property_id: int = None
    ):
        return pasture_repository.get_all(
            db, skip=skip, limit=limit, property_id=property_id
        )

    def get_pasture(self, db: Session, pasture_id: int):
        db_pasture = pasture_repository.get_by_id(db, pasture_id)
        if not db_pasture:
            raise HTTPException(status_code=404, detail="Pasture not found")
        return db_pasture

    def update_pasture(
        self, db: Session, pasture_id: int, pasture_update: PastureUpdate
    ):
        db_pasture = self.get_pasture(
            db, pasture_id
        )  # reutiliza a busca que já lança o erro 404

        # se o usuário tentou mudar a qual fazenda esse pasto pertence, verifica se a nova fazenda existe
        if pasture_update.property_id is not None:
            db_property = PropertyRepository.get_by_id(db, pasture_update.property_id)
            if not db_property:
                raise HTTPException(status_code=404, detail="New property not found")

        return pasture_repository.update(db, db_pasture, pasture_update)

    def delete_pasture(self, db: Session, pasture_id: int):
        db_pasture = self.get_pasture(db, pasture_id)
        return pasture_repository.delete(db, db_pasture)


# instancia unica
pasture_service = PastureService()













