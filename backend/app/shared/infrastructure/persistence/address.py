from sqlalchemy import Column, Integer, String
from app.shared.infrastructure.database.connection import Base # Importa a Base para o mapeamento
from typing import Optional

class Address(Base):
    """
    Modelo de base de dados para endereços.
    """
    __tablename__ = "addresses" # Nome da tabela no MySQL

    # Definição das colunas para o SQLAlchemy
    id_address = Column(Integer, primary_key=True, index=True)
    zip_code = Column(String(20), nullable=False)
    state = Column(String(50), nullable=False)
    neighborhood = Column(String(100), nullable=False)
    street_name = Column(String(150), nullable=False)
    number = Column(String(20), nullable=False)
    complement = Column(String(255), nullable=True)

    def __init__(
        self,
        zip_code: str,
        state: str,
        neighborhood: str,
        street_name: str,
        number: str,
        complement: Optional[str] = None,
        id_address: Optional[int] = None
    ):
        self.id_address = id_address
        self.zip_code = zip_code
        self.state = state
        self.neighborhood = neighborhood
        self.street_name = street_name
        self.number = number
        self.complement = complement









































