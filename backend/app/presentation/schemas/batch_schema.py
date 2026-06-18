from typing import Optional

from pydantic import BaseModel, Field

from app.enums.batch.batch_purpose import BatchPurpose
from app.presentation.schemas.common import BRDate


class BatchBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    batch_purpose: BatchPurpose
    status: str = Field(..., min_length=2, max_length=50)
    category: str = Field(..., min_length=2, max_length=50)
    check_in: BRDate
    check_out: Optional[BRDate] = None


class BatchCreate(BatchBase):
    pass


class BatchUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    batch_purpose: Optional[BatchPurpose] = None
    status: Optional[str] = Field(default=None, min_length=2, max_length=50)
    category: Optional[str] = Field(default=None, min_length=2, max_length=50)
    check_in: Optional[BRDate] = None
    check_out: Optional[BRDate] = None


class BatchResponse(BatchBase):
    id_batch: int

    class Config:
        from_attributes = True









































