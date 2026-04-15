from app.enums.protocolo.protocolo_status import ProtocoloStatus

class Protocolo:

    def __init__(
        self,
        id_protocolo: int,
        nome: str,
        tipo: str,
        protocolo_status: ProtocoloStatus
    ):
        self.id_protocolo = id_protocolo
        self.nome = nome
        self.tipo = tipo
        self.protocolo_status = protocolo_status
        self.etapas = []