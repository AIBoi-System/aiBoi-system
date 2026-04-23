from datetime import date
from typing import Optional

from sqlalchemy import Column, Integer, String, Date, Float, Enum, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.enums.health.health_type import HealthType


class Health(Base):
    """
    Representa os registros sanitários (vacinas, medicamentos, tratamentos) do animal.
    Essencial para o controle de carência e emissão de GTA.
    """
    __tablename__ = "health_records"

    # Identificação
    id_health_record = Column(Integer, primary_key=True, index=True)
    
    # Detalhes do Tratamento
    health_type = Column(Enum(HealthType), nullable=False)
    product_name = Column(String(100), nullable=False)
    application_date = Column(Date, default=date.today, nullable=False)
    responsible = Column(String(100), nullable=True)
    
    # Dosagem e Custos
    dosage = Column(Float, nullable=True)
    unit_price = Column(Float, nullable=True)
    
    notes = Column(Text, nullable=True)

    # Relacionamento com o Animal
    animal_id = Column(Integer, ForeignKey("animals.id_animal"), nullable=False)
    
    # Mapeamento inverso para facilitar consultas
    animal = relationship("Animal", back_populates="health_records")