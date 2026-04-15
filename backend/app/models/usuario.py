from cpf import CPF
from backend.app.models.endereco import Endereco

class Usuario:

    def __init__(
        self,
        id_usuario: int,
        nome: str,
        email: str,
        senha: str,
        telefone: str,
        status_conta: str,
        endereco: Endereco,
        CPF: CPF
    ):
        self.id_usuario = id_usuario
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.status_conta = status_conta
        self.endereco = endereco
        self.CPF = CPF