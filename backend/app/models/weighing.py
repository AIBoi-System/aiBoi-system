from datetime import date


class Weighing:

    def __init__(
        self,
        id: int,
        weight: float,
        weigh_date: date,
        animal_id: int
    ):
        self.id = id
        self.weight = weight
        self.weigh_date = weigh_date

        self.animal_id = animal_id