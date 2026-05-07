from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db

# Adicionado AddressUpdate nos imports
from app.schemas.address_schema import AddressCreate, AddressResponse, AddressUpdate
from app.services.address_service import AddressService

router = APIRouter()


@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    return AddressService.create_address(db, address)


@router.get("/", response_model=list[AddressResponse])
def list_addresses(db: Session = Depends(get_db)):
    return AddressService.get_all_addresses(db)


@router.get("/{address_id}", response_model=AddressResponse)
def get_address(address_id: int, db: Session = Depends(get_db)):
    return AddressService.get_address_by_id(db, address_id)


@router.put("/{address_id}", response_model=AddressResponse)
def update_address(
    address_id: int, address_data: AddressUpdate, db: Session = Depends(get_db)
):
    """
    Atualiza os dados de um endereço existente no AiBoi-system.
    """
    return AddressService.update_address(db, address_id, address_data)


@router.delete("/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    return AddressService.delete_address(db, address_id)
