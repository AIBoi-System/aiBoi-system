from typing import List

from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

from app.modules.inventory.application.use_cases import (
    CreateAnimalUseCase,
    GetAnimalUseCase,
    ListAnimalsUseCase,
    UpdateAnimalUseCase,
    DeleteAnimalUseCase,
)
from app.modules.inventory.domain.entity import Animal
from app.shared.infrastructure.database.connection import get_db
from app.presentation.api.dependencies import (
    get_create_animal_use_case,
    get_get_animal_use_case,
    get_list_animals_use_case,
    get_update_animal_use_case,
    get_delete_animal_use_case,
)
from app.presentation.api.auth_dependencies import get_current_user, verify_property_access
from app.presentation.schemas.animal import AnimalCreate, AnimalResponse, AnimalUpdate
from app.presentation.api.v1.mappers import animal_to_response

router = APIRouter(prefix="/animals", tags=["Animals"])


def _schema_to_entity(schema: AnimalCreate, property_id: int) -> Animal:
    data = schema.model_dump()
    data["property_id"] = property_id
    return Animal.create(**data)


@router.post("/", response_model=AnimalResponse, status_code=status.HTTP_201_CREATED)
def create_animal(
    payload: AnimalCreate,
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    use_case: CreateAnimalUseCase = Depends(get_create_animal_use_case),
):
    verify_property_access(db, property_id, current_user)
    created = use_case.execute(_schema_to_entity(payload, property_id))
    return animal_to_response(created)


@router.get("/", response_model=List[AnimalResponse])
def list_animals(
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    use_case: ListAnimalsUseCase = Depends(get_list_animals_use_case),
):
    verify_property_access(db, property_id, current_user)
    animals = use_case.execute(property_id)
    return [animal_to_response(a) for a in animals]


@router.get("/{animal_id}", response_model=AnimalResponse)
def get_animal(
    animal_id: int,
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    use_case: GetAnimalUseCase = Depends(get_get_animal_use_case),
):
    verify_property_access(db, property_id, current_user)
    animal = use_case.execute(animal_id, property_id)
    return animal_to_response(animal)


@router.put("/{animal_id}", response_model=AnimalResponse)
def update_animal(
    animal_id: int,
    property_id: int,
    payload: AnimalUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    use_case: UpdateAnimalUseCase = Depends(get_update_animal_use_case),
):
    verify_property_access(db, property_id, current_user)
    updated = use_case.execute(animal_id, property_id, payload.model_dump(exclude_unset=True))
    return animal_to_response(updated)


@router.delete("/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_animal(
    animal_id: int,
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    use_case: DeleteAnimalUseCase = Depends(get_delete_animal_use_case),
):
    verify_property_access(db, property_id, current_user)
    use_case.execute(animal_id, property_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)














































