from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates

from app.core.database import Base
from app.models.cpf import CPF


class User(Base):
    """
    Representa a base de usuários do sistema AiBoi.
    Contém informações de login, contato e validação de documentos.
    """
    __tablename__ = "users"

    # Identificação e Login
    id_user = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False) # Armazenar sempre o hash
    
    # Contato e Status
    phone = Column(String(20), nullable=True)
    account_status = Column(String(50), default="Ativo") # Ex: 'Ativo', 'Suspenso'
    
    # Documento com Validação Automatizada
    cpf = Column(String(14), unique=True, nullable=False)

    # Relacionamento com Endereço
    address_id = Column(Integer, ForeignKey("addresses.id_address"), nullable=True)
    address = relationship("Address")

    # Configuração para Herança (Polimorfismo)
    type = Column(String(50)) # Identifica se é 'owner', 'admin', etc.
    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": type
    }

    @validates("cpf")
    def validate_cpf(self, key, value):
        """
        Garante que apenas CPFs válidos e formatados 
        sejam salvos no banco de dados AWS RDS.
        """
        cpf_objeto = CPF(value)
        return str(cpf_objeto)