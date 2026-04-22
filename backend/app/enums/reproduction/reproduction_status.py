from enum import Enum

class ReproductionStatus(Enum):
    IN_PROGRESS = "Em andamento"
    FINISHED  = "Finalizado"
    CANCELLED = "Cancelado"