from dataclasses import dataclass, field

from app.shared.domain.entity import Entity
from app.shared.domain.exceptions import ValidationException
from app.shared.domain.value_objects import (
    BrazilianAddress,
    BrazilianPhone,
    CPF,
    EmailAddress,
)


@dataclass(frozen=True, kw_only=True)
class CompletedRegistration:
    """Immutable contract handed to the application layer for persistence."""

    name: str
    email: str
    phone: str
    cpf: str
    address: BrazilianAddress
    password_hash: str = field(repr=False)


@dataclass(kw_only=True)
class Registration(Entity):
    """Staged registration workflow with verification ordering invariants.

    Proposed application contract:

    1. ``start`` with the e-mail and Brazilian phone destination.
    2. Confirm each destination using ``verify_email`` and ``verify_phone``.
    3. Hash the password outside the domain and call ``set_password_hash``.
    4. Supply personal/address data with ``set_profile``.
    5. Call ``complete`` and persist the returned immutable contract atomically.

    Verification codes and password hashing remain application/infrastructure
    concerns. This object never stores verification codes or plaintext passwords.
    """

    email: EmailAddress
    phone: BrazilianPhone
    _email_verified: bool = field(default=False, init=False)
    _phone_verified: bool = field(default=False, init=False)
    _password_hash: str | None = field(default=None, repr=False)
    _name: str | None = None
    _cpf: CPF | None = None
    _address: BrazilianAddress | None = None

    @classmethod
    def start(cls, *, email: str, phone: str) -> "Registration":
        return cls(email=EmailAddress(email), phone=BrazilianPhone(phone))

    @property
    def email_verified(self) -> bool:
        return self._email_verified

    @property
    def phone_verified(self) -> bool:
        return self._phone_verified

    def verify_email(self, verified_email: str) -> None:
        if EmailAddress(verified_email) != self.email:
            raise ValidationException("E-mail verificado não corresponde ao cadastro.")
        self._email_verified = True

    def verify_phone(self, verified_phone: str) -> None:
        if BrazilianPhone(verified_phone) != self.phone:
            raise ValidationException(
                "Telefone verificado não corresponde ao cadastro."
            )
        self._phone_verified = True

    def set_password_hash(self, password_hash: str) -> None:
        self._ensure_contacts_verified()
        normalized = str(password_hash).strip()
        if not normalized:
            raise ValidationException("Hash de senha é obrigatório.")
        self._password_hash = normalized

    def set_profile(
        self,
        *,
        name: str,
        cpf: str,
        address: BrazilianAddress,
    ) -> None:
        normalized_name = str(name).strip()
        if len(normalized_name) < 3 or len(normalized_name) > 150:
            raise ValidationException("Nome inválido.")
        if not isinstance(address, BrazilianAddress):
            raise ValidationException("Endereço brasileiro inválido.")
        self._name = normalized_name
        self._cpf = CPF(cpf)
        self._address = address

    def complete(self) -> CompletedRegistration:
        self._ensure_contacts_verified()
        if self._password_hash is None:
            raise ValidationException("Senha ainda não foi definida.")
        if self._name is None or self._cpf is None or self._address is None:
            raise ValidationException("Dados pessoais e endereço estão incompletos.")
        return CompletedRegistration(
            name=self._name,
            email=self.email.value,
            phone=self.phone.value,
            cpf=self._cpf.value,
            address=self._address,
            password_hash=self._password_hash,
        )

    def _ensure_contacts_verified(self) -> None:
        if not self._email_verified or not self._phone_verified:
            raise ValidationException(
                "E-mail e telefone devem ser verificados antes de definir a senha."
            )
