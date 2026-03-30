from fastapi import APIRouter

router = APIRouter()

@router.get("/animals")
def list_animals():
    return [{"id": 1, "nome": "Boi 1"}]