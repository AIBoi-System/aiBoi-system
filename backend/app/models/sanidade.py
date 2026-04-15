from datetime import date
from app.enums.sanidade.SanidadeTipo import SanidadeTipo

class Sanidade:

    def __init__(
        self,
        id_sanidade: int,
        sanidade_tipo: SanidadeTipo,
        nome_produto: str,
        data_aplicacao: date,
        responsavel, 
        dosagem: float,
        preco_unitario: float,
        observacao: str
    ):
        self.id_sanidade = id_sanidade
        self.sanidade_tipo = sanidade_tipo
        self.nome_produto = nome_produto
        self.data_aplicacao = data_aplicacao
        self.responsavel = responsavel
        self.dosagem = dosagem
        self.preco_unitario = preco_unitario
        self.observacao = observacao