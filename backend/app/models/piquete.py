from app.enums.piquete.PiqueteStatus import PiqueteStatus

class Piquete:

    def __init__(
        self,
        id: int,
        nome: str,
        area_ha: float,
        tipo_capim: str,
        qualidade_pasto: str,
        observacao: str,
        capacidade_animal: int,
        piquete_status: PiqueteStatus
    ):
        self.id = id
        self.nome = nome
        self.area_ha = area_ha
        self.tipo_capim = tipo_capim
        self.qualidade_pasto = qualidade_pasto
        self.observacao = observacao
        self.capacidade_animal = capacidade_animal
        self.piquete_status = piquete_status