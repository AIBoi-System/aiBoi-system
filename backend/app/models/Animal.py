from datetime import date
from typing import Optional

from app.enums.animal.sexo import Sexo
from app.enums.animal.animalStatus import AnimalStatus
from app.enums.animal.animalPorte import AnimalPorte
from app.enums.animal.categoria import AnimalCategoria
from app.enums.animal.StatusReprodutivo import AnimalStatusReprodutivo
from app.enums.animal.AnimalOrigem import AnimalOrigem


class Animal:

    def __init__(
        self,
        id_Animal: int,
        numero_identificação: int,
        chip: int,
        registro_po: int,
        nome: str,
        sexo: Sexo,
        raca: str,
        categoria: str,
        animal_porte: AnimalPorte,
        animal_status: AnimalStatus,
        anima_status_reprodutivo: AnimalStatusReprodutivo,
        data_nascimento: date,
        animalorigem: AnimalOrigem,
        data_entrada: date,
        data_saida: date,
        data_desmame: date,
        peso_desmama: float,
        peso_nacimento: float,
        OBS: str,
        animal_categoria: AnimalCategoria
    ):
        self.id_Animal = id_Animal
        self.numero_identificação = numero_identificação
        self.chip = chip
        self.registro_po = registro_po
        self.nome = nome
        self.sexo = sexo
        self.raca = raca
        self.categoria = categoria
        self.animal_porte = animal_porte
        self.animal_status = animal_status
        self.anima_status_reprodutivo = anima_status_reprodutivo
        self.data_nascimento = data_nascimento
        self.animalorigem = animalorigem
        self.data_entrada = data_entrada
        self.data_saida = data_saida
        self.data_desmame = data_desmame
        self.peso_desmama = peso_desmama
        self.peso_nacimento = peso_nacimento
        self.OBS = OBS
        self.animal_categoria = animal_categoria