from .animal_base import AnimalBase

class AnimalResponse(AnimalBase):
    id_animal: int

    class Config:
        from_attributes = True










































