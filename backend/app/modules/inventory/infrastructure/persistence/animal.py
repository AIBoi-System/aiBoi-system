from datetime import date
from typing import List, Optional

# Adicionado ForeignKey à lista de imports
from sqlalchemy import Column, Integer, String, Date, Float, Enum, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.shared.infrastructure.database.connection import Base
from app.enums.animal.animal_sex import AnimalSex
from app.enums.animal.animal_life_status import AnimalLifeStatus
from app.enums.animal.animal_size import AnimalSize
from app.enums.animal.animal_category import AnimalCategory
from app.enums.animal.animal_reproductive_status import AnimalReproductiveStatus
from app.enums.animal.animal_origin import AnimalOrigin


class AnimalModel(Base):
    """
    Representa a entidade principal do sistema AiBoi.
    Seguindo as normas do PEP 8 e mapeamento SQLAlchemy.
    """

    __tablename__ = "animals"

    # Identificação
    id_animal = Column(Integer, primary_key=True, index=True)
    identification_number = Column(Integer, nullable=False, unique=True)
    chip_id = Column(Integer, nullable=True)
    pedigree_po = Column(Integer, nullable=True)
    name = Column(String(100), nullable=True)

    # Atributos Bio-Produtivos
    sex = Column(Enum(AnimalSex), nullable=False)
    breed = Column(String(50), nullable=True)
    animal_size = Column(Enum(AnimalSize), nullable=False)

    animal_life_status = Column(
        Enum(AnimalLifeStatus), nullable=False, default=AnimalLifeStatus.ACTIVE
    )

    reproductive_status = Column(Enum(AnimalReproductiveStatus), nullable=True)
    animal_category = Column(Enum(AnimalCategory), nullable=False)

    # Datas e Pesos
    birth_date = Column(Date, nullable=False)
    origin = Column(Enum(AnimalOrigin), nullable=False)
    entry_date = Column(Date, nullable=True)
    exit_date = Column(Date, nullable=True)
    weaning_date = Column(Date, nullable=True)  # Estava 'weining'
    weaning_weight = Column(Float, nullable=True)  # Estava 'weining'
    birth_weight = Column(Float, nullable=True)
    biometric_vector = Column(Text, nullable=True)

    notes = Column(Text, nullable=True)

    # --- CHAVES ESTRANGEIRAS ---
    # Vincula o animal a uma propriedade específica (Isolamento de Dados)
    property_id = Column(Integer, ForeignKey("properties.id_property"), nullable=False)

    # Vincula o animal a um lote específico
    batch_id = Column(Integer, ForeignKey("batches.id_batch"), nullable=True)
    
    # --- RELACIONAMENTOS ---
    property = relationship("Property")
    batch = relationship("Batch", back_populates="animals")

    weights = relationship(
        "Weighing", back_populates="animal", cascade="all, delete-orphan", passive_deletes=True
    )

    health_records = relationship(
        "HealthModel", back_populates="animal", cascade="all, delete-orphan"
    )
    reproductions = relationship("Reproduction", back_populates="animal")
    events = relationship(
        "AnimalEvent", back_populates="animal", cascade="all, delete-orphan"
    )
    movements = relationship("AnimalMovement", back_populates="animal")
    death_record = relationship("DeathRecord", back_populates="animal", uselist=False)










































