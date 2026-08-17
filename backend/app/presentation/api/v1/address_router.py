from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.shared.infrastructure.database.connection import get_db

# Adicionado AddressUpdate nos imports
from app.presentation.schemas.address_schema import AddressCreate, AddressResponse, AddressUpdate
from app.shared.application.address.address_service import AddressService
from app.presentation.api.auth_dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_address(
    address: AddressCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return AddressService.create_address(db, address)


@router.get("/", response_model=list[AddressResponse])
def list_addresses(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.type != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso não autorizado.")
    return AddressService.get_all_addresses(db)


@router.get("/{address_id}", response_model=AddressResponse)
def get_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    owner_id = None if (current_user.type or "").casefold() == "admin" else current_user.id_user
    return AddressService.get_address_by_id(db, address_id, owner_id=owner_id)


@router.put("/{address_id}", response_model=AddressResponse)
def update_address(
    address_id: int,
    address_data: AddressUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Atualiza os dados de um endereço existente no AiBoi-system.
    """
    owner_id = None if (current_user.type or "").casefold() == "admin" else current_user.id_user
    return AddressService.update_address(
        db, address_id, address_data, owner_id=owner_id
    )


@router.delete("/{address_id}")
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.type != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso não autorizado.")
    return AddressService.delete_address(db, address_id)















































