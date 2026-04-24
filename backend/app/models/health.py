from datetime import date
from typing import Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Float,
    Enum as SQLEnum,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.enums.health.health_type import HealthType


class Health(Base):
    """
    Representa os registros sanitários (vacinas, medicamentos, tratamentos).
    Essencial para o controle de carência e emissão de GTA.
    Atualizado para suportar aplicação individual (Animal) ou em massa (Batch).
    """

    __tablename__ = "health_records"

    # Identificação (Mantendo o padrão do Sandro)
    id_health_record = Column(Integer, primary_key=True, index=True)

    # Detalhes do Tratamento
    health_type = Column(SQLEnum(HealthType), nullable=False)
    product_name = Column(String(100), nullable=False)
    application_date = Column(Date, default=date.today, nullable=False)
    responsible = Column(String(100), nullable=True)

    # Dosagem e Custos
    dosage = Column(Float, nullable=True)
    unit_price = Column(Float, nullable=True)

    notes = Column(Text, nullable=True)

    # ==========================================
    # CHAVES ESTRANGEIRAS (Ajustado conforme o Diagrama)
    # ==========================================
    # Alterado para nullable=True (pois o registro pode ser do Lote em vez do Animal)
    animal_id = Column(Integer, ForeignKey("animals.id_animal"), nullable=True)

    # Adicionado o vínculo com o Lote (Batch)
    batch_id = Column(Integer, ForeignKey("batches.id_batch"), nullable=True)

    # Relacionamentos
    animal = relationship("Animal", back_populates="health_records")
    batch = relationship("Batch", back_populates="health_records")
