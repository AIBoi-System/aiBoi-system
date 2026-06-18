import enum


class AnimalLifeStatus(str, enum.Enum):  # Adicionamos o 'str' aqui por boas práticas
    ACTIVE = "ATIVO"
    SOLD = "VENDIDO"
    DEAD = "MORTO"
    SLAUGHTERED = "ABATIDO"
    CULLED = "DESCARTADO"









































