from datetime import date
from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.shared.infrastructure.database.connection import Base
from app.enums.batch.batch_purpose import BatchPurpose


class Batch(Base):
    """
    Representa um lote de animais no sistema AiBoi.
    Organiza os animais por finalidade e status de manejo.
    """

    __tablename__ = "batches"
    __table_args__ = (
        UniqueConstraint(
            "id_batch",
            "property_id",
            name="uq_batches_id_property",
        ),
    )

    # Identificação do Lote
    id_batch = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    # Atributos de Negócio
    batch_purpose = Column(Enum(BatchPurpose), nullable=False)
    status = Column(String(50), nullable=False)  # Ex: 'Ativo', 'Encerrado'
    category = Column(String(50), nullable=False)  # Ex: 'Bezerros', 'Matrizes'

    # Controle Temporal
    check_in = Column(Date, default=date.today, nullable=False)
    check_out = Column(Date, nullable=True)

    # --- CHAVES ESTRANGEIRAS ---
    # Vincula o lote a uma propriedade específica (Isolamento de Dados)
    property_id = Column(Integer, ForeignKey("properties.id_property"), nullable=False, index=True)

    # Relacionamentos
    property = relationship("Property")

    # 1. Lista de animais que pertencem atualmente a este lote
    animals = relationship(
        "AnimalModel",
        back_populates="batch",
        overlaps="property",
    )

    # 2. Histórico de movimentações deste lote entre piquetes
    movements = relationship("BatchMovement", back_populates="batch")

    # 3. Registros sanitários aplicados a este lote (EM MASSA)
    health_records = relationship(
        "HealthModel",
        back_populates="batch",
        overlaps="health_records",
    )









































