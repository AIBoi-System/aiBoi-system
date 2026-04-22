from backend.app.enums.pasture.pasture_management import GrazingManagement


class Pasture:

    def __init__(
        self,
        id_pasture: int,
        name: str,
        area: float,
        notes: str,
        capacity: int,
        grazing_management: GrazingManagement
    ):
        self.id_pasture = id_pasture
        self.name = name
        self.area = area
        self.notes = notes
        self.capacity = capacity
        self.grazing_management = grazing_management