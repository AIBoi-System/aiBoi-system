from datetime import date
from typing import Optional

from sqlalchemy import Column, Integer, Date, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.shared.infrastructure.database.connection import Base


class BatchMovement(Base):
    """
    Representa a movimentação de um lote entre diferentes piquetes (pastos).
    Segue o padrão PEP 8 e mapeamento direto para o AWS RDS.
    """
    __tablename__ = "batch_movements"

    # Identificação do Movimento
    id_movement = Column(Integer, primary_key=True, index=True)
    
    # Chave Estrangeira para o Lote
    batch_id = Column(Integer, ForeignKey("batches.id_batch"), nullable=False)
    
    # Chaves Estrangeiras para os Piquetes (Origem e Destino)
    origin_paddock_id = Column(Integer, ForeignKey("paddocks.id_paddock"), nullable=False)
    destination_paddock_id = Column(Integer, ForeignKey("paddocks.id_paddock"), nullable=False)
    
    # Dados da Movimentação
    movement_date = Column(Date, default=date.today, nullable=False)
    notes = Column(Text, nullable=True)

    # Relacionamentos
    # O SQLAlchemy precisa identificar qual FK usar para cada relação de Paddock
    batch = relationship("Batch", back_populates="movements")
    origin_paddock = relationship("Paddock", foreign_keys=[origin_paddock_id])
    destination_paddock = relationship("Paddock", foreign_keys=[destination_paddock_id])









































