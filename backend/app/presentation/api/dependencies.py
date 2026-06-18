from fastapi import Depends
from sqlalchemy.orm import Session

from app.modules.inventory.application.use_cases import (
    CreateAnimalUseCase,
    GetAnimalUseCase,
    ListAnimalsUseCase,
    UpdateAnimalUseCase,
    DeleteAnimalUseCase,
)
from app.modules.health.application.use_cases import (
    CreateHealthRecordUseCase,
    DeleteHealthRecordUseCase,
    GetHealthRecordUseCase,
    ListHealthRecordsUseCase,
    UpdateHealthRecordUseCase,
)
from app.modules.inventory.domain.repository import AnimalRepository
from app.modules.inventory.domain.animal_domain_service import AnimalDomainService
from app.modules.health.domain.repository import HealthRepository
from app.shared.infrastructure.database.connection import get_db
from app.modules.inventory.infrastructure.persistence.sqlalchemy_animal_repository import (
    SqlAlchemyAnimalRepository,
)
from app.modules.health.infrastructure.persistence.sqlalchemy_health_repository import (
    SqlAlchemyHealthRepository,
)


def get_animal_repository(db: Session = Depends(get_db)) -> AnimalRepository:
    return SqlAlchemyAnimalRepository(db)


def get_health_repository(db: Session = Depends(get_db)) -> HealthRepository:
    return SqlAlchemyHealthRepository(db)


def get_animal_domain_service(
    repo: AnimalRepository = Depends(get_animal_repository),
) -> AnimalDomainService:
    return AnimalDomainService(repo)


def get_create_animal_use_case(
    repo: AnimalRepository = Depends(get_animal_repository),
    service: AnimalDomainService = Depends(get_animal_domain_service),
) -> CreateAnimalUseCase:
    return CreateAnimalUseCase(repo, service)


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
    service: AnimalDomainService = Depends(get_animal_domain_service),
) -> UpdateAnimalUseCase:
    return UpdateAnimalUseCase(repo, service)


def get_delete_animal_use_case(
    repo: AnimalRepository = Depends(get_animal_repository),
) -> DeleteAnimalUseCase:
    return DeleteAnimalUseCase(repo)


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









































