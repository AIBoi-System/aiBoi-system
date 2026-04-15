from enum import Enum

class ProtocoloStatus(Enum):
    NAO_INICIADO = "Nao iniciado"
    EM_ANDAMENTO = "Em andamento"
    FINALIZADO = "Finalizado"
    CANCELADO = "Cancelado"