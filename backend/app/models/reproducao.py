from datetime import date
from backend.app.models import protocolo
from reproducao_tipo import ReproducaoTipo
from reproducao_status import ReproducaoStatus
from reproducao_resultado import ReproducaoResultado


class Reproducao:

    def __init__(
        self,
        id: int,
        reproducaoTipo: ReproducaoTipo,
        data_inicio: date,
        data_fim: date,
        data_diagnostico: date,
        reproducao: ReproducaoStatus,
        reproducaoresultado: ReproducaoResultado,
        observacao: str
    ):
        self.id = id
        self.reproducaoTipo = reproducaoTipo
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.data_diagnostico = data_diagnostico
        self.reproducao = reproducao
        self.reproducaoresultado = reproducaoresultado
        self.observacao = observacao
        self.protocolo = protocolo

        self.etapas_execucao = [] 