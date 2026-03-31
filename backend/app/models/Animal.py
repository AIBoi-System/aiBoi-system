from sqlalchemy import Column, Integer, String, Date, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.core.database import Base

# Enums (domínio centralizado)
from app.enums.sexo import Sexo
from app.enums.status_geral import StatusGeral
from app.enums.status_reprodutivo import StatusReprodutivo
from app.enums.origem import Origem


class Animal(Base):
    __tablename__ = "animals"

    # =========================
    # 🔑 Identificação
    # =========================
    id = Column("id_animal", Integer, primary_key=True, index=True)
    numero_identificacao = Column(Integer, unique=True, nullable=False, index=True)
    chip = Column(Integer, unique=True, nullable=True, index=True)
    registro_po = Column(Integer, nullable=True)

    # =========================
    # 📌 Dados básicos
    # =========================
    nome = Column(String(100), nullable=True)
    sexo = Column(SqlEnum(Sexo), nullable=False)
    raca = Column(String(50), nullable=False)
    categoria = Column(String(50), nullable=False)

    # =========================
    # 📊 Status
    # =========================
    status_geral = Column(SqlEnum(StatusGeral), nullable=False)
    status_reprodutivo = Column(SqlEnum(StatusReprodutivo), nullable=True)

    # =========================
    # 📅 Datas
    # =========================
    data_nascimento = Column(Date, nullable=False)
    data_entrada = Column(Date, nullable=False)
    data_saida = Column(Date, nullable=True)

    # =========================
    # 📍 Origem
    # =========================
    origem = Column(SqlEnum(Origem), nullable=True)

    # =========================
    # 📝 Observação
    # =========================
    observacao = Column(String(255), nullable=True)

    # =========================
    # 🔗 Relacionamentos (FUTURO)
    # =========================
    # pesagens = relationship("Pesagem", back_populates="animal", cascade="all, delete-orphan")
    # eventos = relationship("EventoAnimal", back_populates="animal")

    # =========================
    # 🧠 Métodos de domínio
    # =========================
    def esta_ativo(self) -> bool:
        """
        Verifica se o animal está ativo.
        """
        return self.status_geral == StatusGeral.ATIVO

    def tem_chip(self) -> bool:
        """
        Verifica se o animal possui chip.
        """
        return self.chip is not None

    def idade(self, data_atual) -> int:
        """
        Calcula idade em anos.
        """
        return data_atual.year - self.data_nascimento.year

    def saiu_da_propriedade(self) -> bool:
        """
        Verifica se o animal já saiu (venda/morte).
        """
        return self.data_saida is not None

    def __repr__(self) -> str:
        return f"<Animal(id={self.id}, numero={self.numero_identificacao})>"