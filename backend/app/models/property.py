from app.enums.property.property_type import PropertyType


class Property:

    def __init__(
        self,
        id_property: int,
        name: str,
        property_type: PropertyType,
        area: float
    ):
        self.id_property = id_property
        self.name = name
        self.property_type = property_type
        self.area = area