from cpf import CPF
from app.models.address import Address


class User:

    def __init__(
        self,
        id_user: int,
        name: str,
        email: str,
        password: str,
        phone: str,
        account_status: str,
        address: Address,
        cpf: CPF
    ):
        self.id_user = id_user
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.account_status = account_status
        self.address = address
        self.cpf = cpf