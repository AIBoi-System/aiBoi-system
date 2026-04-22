import enum

class AnimalLifeStatus(enum.Enum):
    ACTIVE = "ATIVO"
    SOLD = "VENDIDO"
    DEAD = "MORTO"
    SLAUGHTERED = "ABATIDO"
    CULLED = "DESCARTADO"