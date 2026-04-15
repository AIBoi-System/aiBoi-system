class Propriedade:

    def __init__(
        self,
        id_propriedade: int,
        nome: str,
        modalidade: str,
        area: float
    ):
        self.id_propriedade = id_propriedade
        self.nome = nome
        self.modalidade = modalidade
        self.area = area

        self.pastagens = [] 