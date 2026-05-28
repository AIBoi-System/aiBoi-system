from typing import Optional

from pydantic import BaseModel, Field

from app.domain.enums.protocol.protocol_status import ProtocolStatus
from app.domain.enums.reproduction.reproduction_result import ReproductionResult
from app.domain.enums.reproduction.reproduction_status import ReproductionStatus
from app.domain.enums.reproduction.reproduction_type import ReproductionType
from app.domain.enums.step.step_name import StepName
from app.domain.enums.step.step_status import StepStatus
from app.domain.enums.stepExecution.step_execultion_result import StepExecultionResult
from app.presentation.schemas.common import BRDate


class ReproductionCreate(BaseModel):
    reproduction_type: ReproductionType
    reproduction_status: ReproductionStatus
    start_date: BRDate
    end_date: Optional[BRDate] = None
    diagnosis_date: Optional[BRDate] = None
    result: Optional[ReproductionResult] = None
    notes: Optional[str] = None
    animal_id: int
    protocol_id: Optional[int] = None


class ReproductionUpdate(BaseModel):
    reproduction_type: Optional[ReproductionType] = None
    reproduction_status: Optional[ReproductionStatus] = None
    start_date: Optional[BRDate] = None
    end_date: Optional[BRDate] = None
    diagnosis_date: Optional[BRDate] = None
    result: Optional[ReproductionResult] = None
    notes: Optional[str] = None
    protocol_id: Optional[int] = None


class ReproductionResponse(ReproductionCreate):
    id: int

    class Config:
        from_attributes = True


class ProtocolCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    type: ReproductionType
    status: ProtocolStatus = ProtocolStatus.NOT_STARTED


class ProtocolResponse(ProtocolCreate):
    id: int

    class Config:
        from_attributes = True


class StepCreate(BaseModel):
    step_name: StepName
    day: BRDate
    status: StepStatus = StepStatus.PENDING
    product_used: Optional[str] = None
    diagnosis_result: Optional[str] = None
    step_date: Optional[BRDate] = None
    implant: Optional[bool] = None
    applied_hormone: Optional[str] = None
    implant_value: Optional[float] = None
    type: Optional[str] = "step"


class StepResponse(StepCreate):
    id: int
    protocol_id: int

    class Config:
        from_attributes = True


class StepExecutionCreate(BaseModel):
    step_id: int
    execution_date: Optional[BRDate] = None
    status: StepStatus
    values: Optional[dict] = None
    result: Optional[StepExecultionResult] = None


class StepExecutionResponse(StepExecutionCreate):
    id: int
    reproduction_id: int

    class Config:
        from_attributes = True


class BirthRecordRequest(BaseModel):
    birth_date: BRDate
    calf_alive: bool
    calf_sex: str = Field(..., pattern="^(M|F)$")
    calf_category: str = Field(..., description="Apenas Novilho(a)/Bezerro(a)")
    notes: Optional[str] = None
