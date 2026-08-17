from sqlalchemy import Column, Integer, Date, Enum, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.shared.infrastructure.database.connection import Base
from app.enums.stepExecution.step_execultion_result import StepExecultionResult
from app.enums.step.step_status import StepStatus


class StepExecution(Base):
    """
    Representa a realização física de uma etapa de protocolo em um ciclo reprodutivo.
    Utiliza um campo JSON para suportar dados variáveis de insumos e exames.
    """
    __tablename__ = "step_executions"

    # Identificação
    id = Column(Integer, primary_key=True, index=True)
    
    # Chaves Estrangeiras
    reproduction_id = Column(
        Integer,
        ForeignKey("reproductions.id"),
        nullable=False,
        index=True,
    )
    step_id = Column(
        Integer,
        ForeignKey("steps.id"),
        nullable=False,
        index=True,
    )
    
    # Dados da Execução
    execution_date = Column(Date, nullable=True)
    status = Column(Enum(StepStatus), nullable=False)
    
    # Armazenamento flexível (hormônios, sêmen, etc.)
    values = Column(JSON().with_variant(JSONB, "postgresql"), nullable=True)
    
    # Resultado técnico (ex: Prenhez Confirmada)
    result = Column(Enum(StepExecultionResult), nullable=True)

    # Relacionamentos
    reproduction = relationship("Reproduction", back_populates="step_executions")
    step = relationship("Step", back_populates="executions")









































