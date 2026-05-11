from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.health_schema import HealthRecordRequest, HealthRecordResponse
from app.services.health_service import create_health_record_service

router = APIRouter(prefix="/health", tags=["Saúde"])


@router.post("/record", response_model=HealthRecordResponse, status_code=201)
def create_health_record(request: HealthRecordRequest, db: Session = Depends(get_db)):
    """
    Criar um novo registro de saúde (vacina, medicamento, tratamento).
    
    O registro pode ser feito para:
    - Um animal específico (animal_id)
    - Um lote inteiro (batch_id)
    
    **Validações:**
    - Deve informar `animal_id` OU `batch_id`, mas não ambos
    - Todos os campos obrigatórios devem ser preenchidos
    
    **Exemplo de requisição (animal individual):**
    ```json
    {
        "health_type": "VACCINE",
        "product_name": "Vacina contra aftosa",
        "dosage": 5.0,
        "animal_id": 1
    }
    ```
    
    **Exemplo de requisição (lote inteiro):**
    ```json
    {
        "health_type": "MEDICATION",
        "product_name": "Vermífugo",
        "dosage": 10.0,
        "batch_id": 5
    }
    ```
    """
    try:
        # Chama o serviço que contém toda a lógica de negócios
        health_record = create_health_record_service(db, request)
        
        # Define o alvo do registro para a resposta
        alvo = (
            f"Animal {request.animal_id}"
            if request.animal_id
            else f"Lote {request.batch_id}"
        )
        
        return HealthRecordResponse(
            message=f"Registro de {request.health_type.value} ({request.product_name}) salvo com sucesso!",
            target=alvo,
        )
    
    except HTTPException:
        # Re-lança exceções HTTP já formatadas pelo serviço
        raise
    
    except Exception as e:
        # Captura e formata qualquer outro erro inesperado
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao registrar saúde: {str(e)}"
        )
