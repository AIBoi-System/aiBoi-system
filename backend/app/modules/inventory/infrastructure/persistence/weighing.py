from datetime import date
from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.shared.infrastructure.database.connection import Base


class Weighing(Base):
    """
    Representa o registro de pesagem de um animal.
    Armazena o peso e a data para monitoramento do desempenho zootécnico.
    """
    __tablename__ = "weighings"

    # Identificação do Registro
    id = Column(Integer, primary_key=True, index=True)
    
    # Dados da Pesagem
    weight = Column(Float, nullable=False)
    weigh_date = Column(Date, default=date.today, nullable=False)

    # Chave Estrangeira para o Animal
    animal_id = Column(Integer, ForeignKey("animals.id_animal"), nullable=False)

    # Relacionamento
    animal = relationship("AnimalModel", back_populates="weights")









































