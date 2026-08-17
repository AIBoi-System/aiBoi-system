import re

from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.shared.infrastructure.database.connection import Base


class CPF(Base):
    """CPF persistido em relação one-to-one com ``User``.

    ``CPF(valor)`` preserva o comportamento histórico de value object, validando
    e formatando o número. O argumento ``number`` é reservado ao adaptador ORM,
    que recebe valores já validados pelos serviços existentes.
    """

    __tablename__ = "cpfs"
    __table_args__ = (UniqueConstraint("number", name="uq_cpfs_number"),)

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id_user",
            name="fk_cpfs_user_id_users",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    number = Column(String(14), nullable=False)

    user = relationship("User", back_populates="cpf_record")

    def __init__(
        self,
        valor: str | None = None,
        *,
        number: str | None = None,
        user_id: int | None = None,
        user=None,
    ):
        if valor is not None and number is not None:
            raise TypeError("Informe valor ou number, não ambos")
        if valor is not None:
            cleaned = self._limpar(str(valor))
            if not self.validar(cleaned):
                raise ValueError("CPF inválido")
            self.number = self.formatar(cleaned)
        elif number is not None:
            self.number = str(number)
        if user_id is not None:
            self.user_id = user_id
        if user is not None:
            self.user = user

    @property
    def valor(self) -> str:
        """Alias compatível com o value object anterior."""
        return self.number

    @valor.setter
    def valor(self, value: str) -> None:
        self.number = value

    def __str__(self) -> str:
        return self.number

    @staticmethod
    def _limpar(valor: str) -> str:
        return re.sub(r"\D", "", valor)

    @staticmethod
    def validar(cpf: str) -> bool:
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False

        first_total = sum(int(cpf[index]) * (10 - index) for index in range(9))
        first_remainder = (first_total * 10) % 11
        first_digit = 0 if first_remainder >= 10 else first_remainder

        second_total = sum(int(cpf[index]) * (11 - index) for index in range(10))
        second_remainder = (second_total * 10) % 11
        second_digit = 0 if second_remainder >= 10 else second_remainder

        return int(cpf[9]) == first_digit and int(cpf[10]) == second_digit

    @staticmethod
    def formatar(cpf: str) -> str:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
