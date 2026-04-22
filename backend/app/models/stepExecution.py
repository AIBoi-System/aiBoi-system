from datetime import date
from typing import Optional, Dict

from backend.app.enums.stepExecution.step_execultion_result import StepExecultionResult


class StepExecution:

    def __init__(
        self,
        id: int,
        reproduction_id: int,
        step_id: int,
        execution_date: Optional[date],
        status: StepStatus,
        values: Optional[Dict] = None,
        result: Optional[StepExecultionResult] = None
    ):
        self.id = id
        self.reproduction_id = reproduction_id
        self.step_id = step_id
        self.execution_date = execution_date
        self.status = status

        # JSON flexível (hormônios, sêmen, etc)
        self.values = values or {}

        # Resultado (apenas no diagnóstico)
        self.result = result