from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Boolean,
    Float,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship
from app.infrastructure.database.connection import Base

# Importando os Enums que criamos nas pastas de domínio
from app.domain.enums.step.step_name import StepName
from app.domain.enums.step.step_status import StepStatus


class Step(Base):
    """
    Representa uma etapa específica dentro de um protocolo reprodutivo.
    Esta é a classe pai que contém os atributos comuns a todas as etapas.
    """

    __tablename__ = "steps"

    # Identificação da Etapa
    id = Column(Integer, primary_key=True, index=True)
    protocol_id = Column(Integer, ForeignKey("protocols.id"), nullable=False)

    # Atributos fiéis ao Diagrama de Classes
    step_name = Column(SQLEnum(StepName), nullable=False)
    day = Column(Date, nullable=False)  # Data prevista para a etapa
    status = Column(SQLEnum(StepStatus), nullable=False)
    product_used = Column(String(100))
    diagnosis_result = Column(String(255), nullable=True)

    # Atributos específicos das subclasses (definidos como opcionais na tabela única)
    step_date = Column(Date, nullable=True)  # Data real da execução
    implant = Column(Boolean, nullable=True)
    applied_hormone = Column(String(100), nullable=True)
    implant_value = Column(Float, nullable=True)

    # Configuração de Herança (Polimorfismo)
    # A coluna 'type' dirá ao SQLAlchemy se a linha é um StageZero, StageEight, etc.
    type = Column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "step",
        "polymorphic_on": type,
    }

    # Relacionamentos (Mantendo o que o Sandro já tinha feito)
    protocol = relationship("Protocol", back_populates="steps")
    executions = relationship("StepExecution", back_populates="step")


# --- SUBCLASSES (Fiéis ao Diagrama de Classes em Inglês) ---


class StageZero(Step):
    """Representa o Dia 0 do Protocolo"""

    __mapper_args__ = {"polymorphic_identity": "stage_zero"}


class StageEight(Step):
    """Representa o Dia 8 do Protocolo"""

    __mapper_args__ = {"polymorphic_identity": "stage_eight"}


class StageTen(Step):
    """Representa o Dia 10 do Protocolo"""

    __mapper_args__ = {"polymorphic_identity": "stage_ten"}


class Diagnosis(Step):
    """Representa a etapa de Diagnóstico Final"""

    __mapper_args__ = {"polymorphic_identity": "diagnosis"}
