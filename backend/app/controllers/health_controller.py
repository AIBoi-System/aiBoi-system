from fastapi import APIRouter, HTTPException
from app.schemas.health_schema import HealthRecordRequest, HealthRecordResponse

router = APIRouter(prefix="/health", tags=["Saúde"])


@router.post("/record", response_model=HealthRecordResponse)
def create_health_record(request: HealthRecordRequest):

    # Validação de Negócio: Não pode mandar os dois vazios!
    if not request.animal_id and not request.batch_id:
        raise HTTPException(
            status_code=400,
            detail="Erro: Você deve informar o animal_id ou o batch_id para registrar a saúde.",
        )

    # Validação de Negócio: Não pode mandar os dois ao mesmo tempo!
    if request.animal_id and request.batch_id:
        raise HTTPException(
            status_code=400,
            detail="Erro: Informe apenas o animal_id OU o batch_id, não ambos.",
        )

    # Define para quem foi a vacina apenas para a mensagem de retorno
    alvo = (
        f"Animal {request.animal_id}"
        if request.animal_id
        else f"Lote {request.batch_id}"
    )

    return HealthRecordResponse(
        message=f"Registro de {request.health_type.value} ({request.product_name}) salvo com sucesso!",
        target=alvo,
    )
