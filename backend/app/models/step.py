class Step:

    def __init__(
        self,
        id: int,
        protocol_id: int,
        name: str,
        order: int
    ):
        self.id = id
        self.protocol_id = protocol_id
        self.name = name
        self.order = order