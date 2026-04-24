from fastapi import APIRouter, HTTPException
from app.enums.step.step_status import StepStatus
from app.enums.health.health_type import HealthType
from app.schemas.reproduction_schema import (
    ProtocolStartRequest,
    ProtocolResponse,
    StepUpdateRequest,
)
from app.services.reproduction_service import ReproductionService

# Cria a "porta" para o módulo de reprodução
router = APIRouter(prefix="/reproductions", tags=["Reprodução"])


@router.post("/start-protocol", response_model=ProtocolResponse)
def start_protocol(request: ProtocolStartRequest):

    # Simulação dos dados que viriam do Banco de Dados (Classe Animal e Fazenda)
    animal_mock_db = {"active": True, "gender": "F", "status": "VAZIA"}
    modulos_contratados_db = ["IATF", "TE", "FIV"]

    try:
        # Passando os dados do Schema para o Service avaliar
        ReproductionService.validate_protocol_start(
            animal_active=animal_mock_db["active"],
            animal_gender=animal_mock_db["gender"],
            animal_status=animal_mock_db["status"],
            protocol_type=request.protocol_type,
            contracted_modules=modulos_contratados_db,
        )
    except ValueError as e:
        # Se a vaca for macho, inativa ou prenhe, o FastAPI devolve Erro 400
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        # Se tentar usar um módulo não pago, devolve Erro 403 (Proibido)
        raise HTTPException(status_code=403, detail=str(e))

    # Se não estourou nenhum erro, o Cérebro aprovou e o Schema empacota a resposta
    return ProtocolResponse(
        message="Protocolo aprovado com sucesso pelas regras biológicas e financeiras!",
        animal_id=request.animal_id,
        protocol=request.protocol_type.value,
        status="PENDING",
    )


@router.put("/step/{step_id}/status")
def update_step_status(step_id: int, request: StepUpdateRequest):

    # SIMULAÇÃO: O banco de dados nos diz que essa Etapa 15 é a aplicação de um hormônio na Vaca 1
    etapa_mock_db = {
        "animal_id": 1,
        "step_name": "APLICAÇÃO DE HORMÔNIO (Prostaglandina)",
        "is_medication": True,  # A flag que diz que isso afeta a saúde!
    }

    # Resposta base
    response_data = {
        "message": f"Status da etapa {step_id} alterado para {request.status.value}.",
        "notes_saved": request.notes,
        "health_integration": "Nenhuma ação de saúde necessária para esta etapa.",
    }

    # O CRUZAMENTO DE DADOS
    # Se o pecuarista marcou como CONCLUÍDO e a etapa for um medicamento:
    if request.status == StepStatus.COMPLETED and etapa_mock_db["is_medication"]:

        # Na vida real, chamaríamos: HealthService.create_record(...)
        # Aqui, vamos gerar o registro automático de Saúde e mostrar na resposta
        registro_saude_gerado = {
            "animal_id": etapa_mock_db["animal_id"],
            "health_type": HealthType.MEDICATION.value,
            "product": etapa_mock_db["step_name"],
            "status_sistema": "SALVO AUTOMATICAMENTE NO PRONTUÁRIO",
        }

        response_data["health_integration"] = registro_saude_gerado
        response_data["message"] = (
            "SUCESSO DUPLO! Etapa concluída e Prontuário de Saúde atualizado sozinho!"
        )

    return response_data
