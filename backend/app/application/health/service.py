from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.infrastructure.persistence.repositories.health_repository import HealthRepository
from app.presentation.schemas.health.health_create import HealthCreate
from app.presentation.schemas.health.health_update import HealthUpdate


class HealthService:

    @staticmethod
    def create(db: Session, data: HealthCreate):
        if not data.animal_id and not data.batch_id:
            raise HTTPException(
                status_code=400,
                detail="Informe animal_id ou batch_id."
            )

        if data.animal_id and data.batch_id:
            raise HTTPException(
                status_code=400,
                detail="Informe apenas animal_id OU batch_id, não ambos."
            )

        return HealthRepository.create(db, data)

    @staticmethod
    def get_all(db: Session):
        return HealthRepository.get_all(db)

    @staticmethod
    def get_by_id(db: Session, health_id: int):
        health = HealthRepository.get_by_id(db, health_id)

        if not health:
            raise HTTPException(
                status_code=404,
                detail="Registro de saúde não encontrado."
            )

        return health

    @staticmethod
    def update(db: Session, health_id: int, data: HealthUpdate):
        health = HealthRepository.update(db, health_id, data)

        if not health:
            raise HTTPException(
                status_code=404,
                detail="Registro de saúde não encontrado."
            )

        return health

    @staticmethod
    def delete(db: Session, health_id: int):
        health = HealthRepository.delete(db, health_id)

        if not health:
            raise HTTPException(
                status_code=404,
                detail="Registro de saúde não encontrado."
            )

        return {"message": "Registro de saúde deletado com sucesso."}
