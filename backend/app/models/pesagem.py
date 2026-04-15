from datetime import date

class Pesagem:

    def __init__(
        self,
        id: int,
        peso: float,
        data: date
    ):
        self.id = id
        self.peso = peso
        self.data = data