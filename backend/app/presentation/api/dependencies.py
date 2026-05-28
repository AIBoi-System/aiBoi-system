from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.animal.use_cases import (
    CreateAnimalUseCase,
    GetAnimalUseCase,
    ListAnimalsUseCase,
    UpdateAnimalUseCase,
)
from app.application.health.use_cases import (
    CreateHealthRecordUseCase,
    DeleteHealthRecordUseCase,
    GetHealthRecordUseCase,
    ListHealthRecordsUseCase,
    UpdateHealthRecordUseCase,
)
from app.domain.animal.repository import AnimalRepository
from app.domain.health.repository import HealthRepository
from app.infrastructure.database.connection import get_db
from app.infrastructure.persistence.repositories.sqlalchemy_animal_repository import (
    SqlAlchemyAnimalRepository,
)
from app.infrastructure.persistence.repositories.sqlalchemy_health_repository import (
    SqlAlchemyHealthRepository,
)


def get_animal_repository(db: Session = Depends(get_db)) -> AnimalRepository:
    return SqlAlchemyAnimalRepository(db)


def get_health_repository(db: Session = Depends(get_db)) -> HealthRepository:
    return SqlAlchemyHealthRepository(db)


def get_create_animal_use_case(
    repo: AnimalRepository = Depends(get_animal_repository),
) -> CreateAnimalUseCase:
    return CreateAnimalUseCase(repo)


def get_list_animals_use_case(
    repo: AnimalRepository = Depends(get_animal_repository),
) -> ListAnimalsUseCase:
    return ListAnimalsUseCase(repo)


def get_get_animal_use_case(
    repo: AnimalRepository = Depends(get_animal_repository),
) -> GetAnimalUseCase:
    return GetAnimalUseCase(repo)


def get_update_animal_use_case(
    repo: AnimalRepository = Depends(get_animal_repository),
) -> UpdateAnimalUseCase:
    return UpdateAnimalUseCase(repo)


def get_create_health_use_case(
    repo: HealthRepository = Depends(get_health_repository),
) -> CreateHealthRecordUseCase:
    return CreateHealthRecordUseCase(repo)


def get_list_health_use_case(
    repo: HealthRepository = Depends(get_health_repository),
) -> ListHealthRecordsUseCase:
    return ListHealthRecordsUseCase(repo)


def get_get_health_use_case(
    repo: HealthRepository = Depends(get_health_repository),
) -> GetHealthRecordUseCase:
    return GetHealthRecordUseCase(repo)


def get_update_health_use_case(
    repo: HealthRepository = Depends(get_health_repository),
) -> UpdateHealthRecordUseCase:
    return UpdateHealthRecordUseCase(repo)


def get_delete_health_use_case(
    repo: HealthRepository = Depends(get_health_repository),
) -> DeleteHealthRecordUseCase:
    return DeleteHealthRecordUseCase(repo)
