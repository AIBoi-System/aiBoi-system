from enum import Enum


class SystemModule(str, Enum):
    IATF = "IATF"
    TE = "TE"
    FIV = "FIV"
    EMPLOYEES = "FUNCIONARIOS"
    RFID = "BRINCOS_RFID"
    DIGITAL_WEIGHING = "PESAGEM_DIGITAL"
    AI_WEIGHING = "PESAGEM_IA"
