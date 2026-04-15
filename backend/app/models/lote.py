from datetime import date
from app.enums.lote.lote_finalidade import LoteFinalidade

class Lote:

    def __init__(
        self,
        id_lote: int,
        nome: str,
        lote_finalidade: LoteFinalidade,
        data_inicio: date,
        data_fim: date,
        status: str,
        categoria: str
    ):
        self.id_lote = id_lote
        self.nome = nome
        self.lote_finalidade = lote_finalidade
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.status = status
        self.categoria = categoria

        self.animais = []  