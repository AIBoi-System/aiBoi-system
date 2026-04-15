from datetime import date
from app.enums.etapa.etapa_status import EtapaStatus

class Etapa:

    def __init__(
        self,
        id_etapa: int,
        nome: str,             
        ordem: int,             
        data_prevista: date,
        data_realizada: date,
        etapa_status: EtapaStatus,
        observacao: str
    ):
        self.id_etapa = id_etapa
        self.nome = nome
        self.ordem = ordem
        self.data_prevista = data_prevista
        self.data_realizada = data_realizada
        self.etapa_status = etapa_status
        self.observacao = observacao