from enum import Enum


class StepStatus(Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    DELAYED = "Delayed"
