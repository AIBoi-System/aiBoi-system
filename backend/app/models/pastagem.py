from app.enums.pastagem.pastagemManejo import Tipo_manejo

class Pastagem:

    def __init__(
        self,
        id_pastagem: int,
        nome: str,
        area: int,
        observacao: str,
        capacidade: str,
        tipo_manejo: Tipo_manejo
    ):
        self.id_pastagem = id_pastagem
        self.nome = nome
        self.area = area
        self.observacao = observacao
        self.capacidade = capacidade
        self.tipo_manejo = tipo_manejo