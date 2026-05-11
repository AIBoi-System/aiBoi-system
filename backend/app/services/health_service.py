from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import date
import logging

from app.repositories.health_repository import (
    create_health_record,
    get_health_record_by_id,
    get_health_records_by_animal,
    get_health_records_by_batch,
    get_all_health_records,
    update_health_record,
    delete_health_record,
)

logger = logging.getLogger(__name__)


def create_health_record_service(db: Session, data):
    """
    Serviço para criar um registro de saúde (vacina, medicamento, tratamento).
    
    Validações:
    - Garante que animal_id OU batch_id foi informado (não ambos, não nenhum)
    - Converte dados do schema para dicionário
    - Salva no banco através do repository
    
    Args:
        db: Sessão do banco de dados
        data: Schema HealthRecordRequest já validado pelo FastAPI
        
    Returns:
        Objeto Health criado
        
    Raises:
        HTTPException: Se validações falharem
    """
    
    # 1. VALIDAÇÃO: Garante que pelo menos um ID foi informado
    if not data.animal_id and not data.batch_id:
        logger.warning("Erro: Nenhum animal_id ou batch_id foi fornecido")
        raise HTTPException(
            status_code=400,
            detail="Erro: Você deve informar o animal_id ou o batch_id para registrar a saúde.",
        )
    
    # 2. VALIDAÇÃO: Garante que não foram informados os dois ao mesmo tempo
    if data.animal_id and data.batch_id:
        logger.warning(f"Erro: Ambos animal_id ({data.animal_id}) e batch_id ({data.batch_id}) foram fornecidos")
        raise HTTPException(
            status_code=400,
            detail="Erro: Informe apenas o animal_id OU o batch_id, não ambos.",
        )
    
    # 3. PREPARAR DADOS: Transformar schema em dicionário
    health_dict = data.dict()
    
    # 4. ADICIONAR DATA DE APLICAÇÃO se não foi enviada
    if "application_date" not in health_dict or health_dict["application_date"] is None:
        health_dict["application_date"] = date.today()
    
    # 5. SALVAR NO BANCO via repository
    try:
        health_record = create_health_record(db, health_dict)
        logger.info(
            f"Registro de saúde criado com sucesso: "
            f"ID={health_record.id_health_record}, "
            f"Tipo={health_record.health_type}, "
            f"Produto={health_record.product_name}"
        )
        return health_record
    
    except Exception as e:
        logger.error(f"Erro ao criar registro de saúde: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao salvar registro de saúde: {str(e)}"
        )


def list_health_records_service(db: Session):
    """
    Serviço para listar todos os registros de saúde.
    
    Returns:
        Lista de registros de saúde
    """
    try:
        records = get_all_health_records(db)
        logger.info(f"Total de registros de saúde recuperados: {len(records)}")
        return records
    except Exception as e:
        logger.error(f"Erro ao listar registros de saúde: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Erro ao recuperar registros de saúde"
        )


def get_health_record_service(db: Session, health_id: int):
    """
    Serviço para buscar um registro de saúde específico.
    
    Args:
        db: Sessão do banco de dados
        health_id: ID do registro de saúde
        
    Returns:
        Objeto Health encontrado
        
    Raises:
        HTTPException: Se o registro não for encontrado
    """
    try:
        health = get_health_record_by_id(db, health_id)
        if not health:
            logger.warning(f"Registro de saúde não encontrado: ID={health_id}")
            raise HTTPException(
                status_code=404,
                detail=f"Registro de saúde com ID {health_id} não encontrado"
            )
        return health
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar registro de saúde {health_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Erro ao recuperar registro de saúde"
        )


def get_health_records_by_animal_service(db: Session, animal_id: int):
    """
    Serviço para listar todos os registros de saúde de um animal.
    
    Args:
        db: Sessão do banco de dados
        animal_id: ID do animal
        
    Returns:
        Lista de registros de saúde do animal
    """
    try:
        records = get_health_records_by_animal(db, animal_id)
        logger.info(f"Registros de saúde do animal {animal_id}: {len(records)} encontrados")
        return records
    except Exception as e:
        logger.error(f"Erro ao buscar registros de saúde do animal {animal_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Erro ao recuperar registros de saúde do animal"
        )


def get_health_records_by_batch_service(db: Session, batch_id: int):
    """
    Serviço para listar todos os registros de saúde de um lote.
    
    Args:
        db: Sessão do banco de dados
        batch_id: ID do lote
        
    Returns:
        Lista de registros de saúde do lote
    """
    try:
        records = get_health_records_by_batch(db, batch_id)
        logger.info(f"Registros de saúde do lote {batch_id}: {len(records)} encontrados")
        return records
    except Exception as e:
        logger.error(f"Erro ao buscar registros de saúde do lote {batch_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Erro ao recuperar registros de saúde do lote"
        )


def update_health_record_service(db: Session, health_id: int, data):
    """
    Serviço para atualizar um registro de saúde.
    
    Args:
        db: Sessão do banco de dados
        health_id: ID do registro de saúde
        data: Schema com os dados a atualizar
        
    Returns:
        Objeto Health atualizado
        
    Raises:
        HTTPException: Se o registro não for encontrado
    """
    try:
        health = get_health_record_by_id(db, health_id)
        if not health:
            logger.warning(f"Registro de saúde não encontrado para atualização: ID={health_id}")
            raise HTTPException(
                status_code=404,
                detail=f"Registro de saúde com ID {health_id} não encontrado"
            )
        
        # Transforma schema em dicionário (apenas campos enviados)
        update_data = data.dict(exclude_unset=True)
        
        # Atualiza através do repository
        updated_health = update_health_record(db, health_id, update_data)
        logger.info(f"Registro de saúde atualizado: ID={health_id}")
        return updated_health
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar registro de saúde {health_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Erro ao atualizar registro de saúde"
        )


def delete_health_record_service(db: Session, health_id: int):
    """
    Serviço para deletar um registro de saúde.
    
    Args:
        db: Sessão do banco de dados
        health_id: ID do registro de saúde
        
    Raises:
        HTTPException: Se o registro não for encontrado
    """
    try:
        health = get_health_record_by_id(db, health_id)
        if not health:
            logger.warning(f"Registro de saúde não encontrado para deleção: ID={health_id}")
            raise HTTPException(
                status_code=404,
                detail=f"Registro de saúde com ID {health_id} não encontrado"
            )
        
        delete_health_record(db, health_id)
        logger.info(f"Registro de saúde deletado: ID={health_id}")
        return {"message": "Registro de saúde deletado com sucesso"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar registro de saúde {health_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Erro ao deletar registro de saúde"
        )
