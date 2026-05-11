from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories import animal_repository

def create_animal_service(db: Session, animal_schema):
    # Regra: identification_number deve ser único
    existing = animal_repository.get_animal_by_identification(db, animal_schema.identification_number)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O número {animal_schema.identification_number} já existe."
        )
    return animal_repository.create_animal(db, animal_schema.dict())

def list_animals_service(db: Session):
    return animal_repository.get_all_animals(db)

def get_animal_service(db: Session, id_animal: int):
    animal = animal_repository.get_animal_by_id(db, id_animal)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal não encontrado.")
    return animal

def update_animal_service(db: Session, id_animal: int, update_data):
    animal = get_animal_service(db, id_animal)
    data = update_data.dict(exclude_unset=True)
    return animal_repository.update_animal(db, id_animal, data)