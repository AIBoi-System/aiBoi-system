from datetime import date
from typing import Optional

class AnimalEvent:
    """
    Classe abstrata/base para o histórico de eventos de um animal.
    Consolida eventos de pesagem, sanidade, reprodução e movimentação de lotes.
    """
    def __init__(
        self,
        id_event: int,
        event_date: date,
        event_type: str, # Ex: 'PESAGEM', 'SANIDADE', 'REPRODUCAO', 'LOTE'
        animal_id: int, 
        description: Optional[str] = None,
        weighing_id: Optional[int] = None,   
        health_id: Optional[int] = None,     
        reproduction_id: Optional[int] = None, 
        batch_id: Optional[int] = None       
    ):
        self.id_event = id_event
        self.event_date = event_date
        self.event_type = event_type
        self.animal_id = animal_id
        self.description = description
        
     
        self.weighing_id = weighing_id
        self.health_id = health_id
        self.reproduction_id = reproduction_id
        self.batch_id = batch_id