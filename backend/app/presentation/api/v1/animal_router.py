from typing import List

from fastapi import APIRouter, Depends, status

from app.application.animal.use_cases import (
    CreateAnimalUseCase,
    GetAnimalUseCase,
    ListAnimalsUseCase,
    UpdateAnimalUseCase,
)
from app.domain.animal.entity import Animal
from app.presentation.api.dependencies import (
    get_create_animal_use_case,
    get_get_animal_use_case,
    get_list_animals_use_case,
    get_update_animal_use_case,
)
from app.presentation.schemas.animal import AnimalCreate, AnimalResponse, AnimalUpdate

router = APIRouter(prefix="/animals", tags=["Animals"])


def _schema_to_entity(schema: AnimalCreate) -> Animal:
    return Animal(**schema.model_dump())


@router.post("/", response_model=AnimalResponse, status_code=status.HTTP_201_CREATED)
def create_animal(
    payload: AnimalCreate,
    use_case: CreateAnimalUseCase = Depends(get_create_animal_use_case),
):
    created = use_case.execute(_schema_to_entity(payload))
    return AnimalResponse.model_validate(created)


@router.get("/", response_model=List[AnimalResponse])
def list_animals(
    use_case: ListAnimalsUseCase = Depends(get_list_animals_use_case),
):
    animals = use_case.execute()
    return [AnimalResponse.model_validate(a) for a in animals]


@router.get("/{animal_id}", response_model=AnimalResponse)
def get_animal(
    animal_id: int,
    use_case: GetAnimalUseCase = Depends(get_get_animal_use_case),
):
    animal = use_case.execute(animal_id)
    return AnimalResponse.model_validate(animal)


@router.put("/{animal_id}", response_model=AnimalResponse)
def update_animal(
    animal_id: int,
    payload: AnimalUpdate,
    use_case: UpdateAnimalUseCase = Depends(get_update_animal_use_case),
):
    updated = use_case.execute(animal_id, payload.model_dump(exclude_unset=True))
    return AnimalResponse.model_validate(updated)
