from app.enums.paddock.paddocke_status import PaddockeStatus


class Paddock:

    def __init__(
        self,
        id_paddock: int,
        name: str,
        area_ha: float,
        grass_type: str,
        forage_quality: str,
        notes: str,
        animal_capacity: int,
        paddock_status: PaddockeStatus
    ):
        self.id_paddock = id_paddock
        self.name = name
        self.area_ha = area_ha
        self.grass_type = grass_type
        self.forage_quality = forage_quality
        self.notes = notes
        self.animal_capacity = animal_capacity
        self.paddock_status = paddock_status