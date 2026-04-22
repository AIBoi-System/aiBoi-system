from enum import Enum

class ProtocolStatus(Enum):
    NOT_STARTED = "Nao iniciado"
    IN_PROGRESS = "Em andamento"
    FINISHED = "Finalizado"
    CANCELLED = "Cancelado"