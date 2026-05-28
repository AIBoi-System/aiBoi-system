from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.infrastructure.persistence.repositories.paddock_repository import paddock_repository
from app.infrastructure.persistence.repositories.property_repository import PropertyRepository
from app.infrastructure.persistence.repositories.pasture_repository import pasture_repository
from app.presentation.schemas.paddock_schema import PaddockCreate, PaddockUpdate


class PaddockService:
    def create_paddock(self, db: Session, paddock: PaddockCreate):
        # a propriedade informada existe?
        db_property = PropertyRepository.get_by_id(db, paddock.property_id)
        if not db_property:
            raise HTTPException(status_code=404, detail="Property not found")

        # se o usuário vinculou o piquete a um pasto, esse pasto existe?
        if paddock.pasture_id:
            db_pasture = pasture_repository.get_by_id(db, paddock.pasture_id)
            if not db_pasture:
                raise HTTPException(status_code=404, detail="Pasture not found")

            # o pasto pertence à mesma fazenda que o usuário informou?
            if db_pasture.property_id != paddock.property_id:
                raise HTTPException(
                    status_code=400,
                    detail="Pasture does not belong to the specified Property",
                )

        return paddock_repository.create(db, paddock)

    def get_paddocks(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        property_id: int = None,
        pasture_id: int = None,
    ):
        return paddock_repository.get_all(
            db, skip=skip, limit=limit, property_id=property_id, pasture_id=pasture_id
        )

    def get_paddock(self, db: Session, paddock_id: int):
        db_paddock = paddock_repository.get_by_id(db, paddock_id)
        if not db_paddock:
            raise HTTPException(status_code=404, detail="Paddock not found")
        return db_paddock

    def update_paddock(
        self, db: Session, paddock_id: int, paddock_update: PaddockUpdate
    ):
        db_paddock = self.get_paddock(db, paddock_id)

        # validações de atualização caso existam mudanças de IDs
        if paddock_update.property_id is not None:
            if not PropertyRepository.get_by_id(db, paddock_update.property_id):
                raise HTTPException(status_code=404, detail="New property not found")

        if paddock_update.pasture_id is not None:
            if not PropertyRepository.get_by_id(db, paddock_update.property_id):
                raise HTTPException(status_code=404, detail="New pasture not found")

        return paddock_repository.update(db, db_paddock, paddock_update)

    def delete_paddock(self, db: Session, paddock_id: int):
        db_paddock = self.get_paddock(db, paddock_id)
        return paddock_repository.delete(db, db_paddock)


# instancia unica
paddock_service = PaddockService()

