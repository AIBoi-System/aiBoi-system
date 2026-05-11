
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Importando seus schemas e dependências
from app.schemas.animal import AnimalCreate, AnimalResponse, AnimalUpdate
from app.services import animal_service
from app.core.database import get_db

router = APIRouter(prefix="/animals", tags=["Animals"])

@router.post("/", response_model=AnimalResponse, status_code=status.HTTP_201_CREATED)
def create_animal(animal: AnimalCreate, db: Session = Depends(get_db)):
    """
    Cria um novo animal no sistema aiBoi.
    Valida duplicidade de identification_number no Service.
    """
    return animal_service.create_animal_service(db, animal)

@router.get("/", response_model=List[AnimalResponse])
def list_animals(db: Session = Depends(get_db)):
    """
    Retorna a lista de todos os animais cadastrados.
    """
    return animal_service.list_animals_service(db)

@router.get("/{id}", response_model=AnimalResponse)
def get_animal(id: int, db: Session = Depends(get_db)):
    """
    Busca um animal específico pelo ID interno.
    """
    return animal_service.get_animal_service(db, id)

@router.put("/{id}", response_model=AnimalResponse)
def update_animal(id: int, animal_data: AnimalUpdate, db: Session = Depends(get_db)):
    """
    Atualiza dados de um animal existente.
    """
    return animal_service.update_animal_service(db, id, animal_data)