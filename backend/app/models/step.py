from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Step(Base):
    """
    Representa uma etapa específica dentro de um protocolo reprodutivo.
    Define a ordem e a descrição da ação a ser realizada.
    """
    __tablename__ = "steps"

    # Identificação da Etapa
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    
    # Ordem de execução ou dia do protocolo (ex: 0, 7, 9)
    step_order = Column(Integer, nullable=False)

    # Chave Estrangeira para o Protocolo Pai
    protocol_id = Column(Integer, ForeignKey("protocols.id"), nullable=False)

    # Relacionamentos
    protocol = relationship("Protocol", back_populates="steps")
    
    # Relacionamento com as execuções reais no campo
    executions = relationship("StepExecution", back_populates="step")