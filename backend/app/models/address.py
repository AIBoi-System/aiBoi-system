from typing import Optional


class Address:

    def __init__(
        self,
        id_address: int,
        zip_code: str,
        state: str,
        neighborhood: str,
        street_name: str,
        number: str,
        complement: Optional[str] = None
    ):
        self.id_address = id_address
        self.zip_code = zip_code
        self.state = state
        self.neighborhood = neighborhood
        self.street_name = street_name
        self.number = number
        self.complement = complement