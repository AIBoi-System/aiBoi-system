from datetime import date
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Float,
    Enum as SQLEnum,
    Text,
    ForeignKey,
    ForeignKeyConstraint,
    Numeric,
)
from sqlalchemy.orm import relationship

from app.shared.infrastructure.database.connection import Base
from app.enums.health.health_type import HealthType


class HealthModel(Base):
    """
    Representa os registros sanitários (vacinas, medicamentos, tratamentos).
    Essencial para o controle de carência e emissão de GTA.
    Atualizado para suportar aplicação individual (Animal) ou em massa (Batch).
    """

    __tablename__ = "health_records"
    __table_args__ = (
        ForeignKeyConstraint(
            ["animal_id", "property_id"],
            ["animals.id_animal", "animals.property_id"],
            name="fk_health_animal_property",
        ),
        ForeignKeyConstraint(
            ["batch_id", "property_id"],
            ["batches.id_batch", "batches.property_id"],
            name="fk_health_batch_property",
        ),
    )

    # Identificação (Mantendo o padrão do Sandro)
    id_health_record = Column(Integer, primary_key=True, index=True)

    # Detalhes do Tratamento
    health_type = Column(SQLEnum(HealthType), nullable=False)
    product_name = Column(String(100), nullable=False)
    application_date = Column(Date, default=date.today, nullable=False)
    responsible = Column(String(100), nullable=True)

    # Dosagem e Custos
    dosage = Column(Float, nullable=True)
    unit_price = Column(Numeric(12, 2), nullable=True)

    notes = Column(Text, nullable=True)

    # ==========================================
    # CHAVES ESTRANGEIRAS (Ajustado conforme o Diagrama)
    # ==========================================
    # Vincula o registro a uma propriedade específica (Isolamento de Dados)
    property_id = Column(Integer, ForeignKey("properties.id_property"), nullable=False, index=True)

    # Alterado para nullable=True (pois o registro pode ser do Lote em vez do Animal)
    animal_id = Column(Integer, nullable=True)

    # Adicionado o vínculo com o Lote (Batch)
    batch_id = Column(Integer, nullable=True)

    # Relacionamentos
    animal = relationship(
        "AnimalModel",
        back_populates="health_records",
        overlaps="health_records",
    )
    batch = relationship(
        "Batch",
        back_populates="health_records",
        overlaps="animal,health_records",
    )









































