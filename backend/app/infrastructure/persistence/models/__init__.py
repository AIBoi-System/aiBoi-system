"""Modelos ORM — importados no bootstrap para create_all."""

from app.infrastructure.persistence.models.address import Address
from app.infrastructure.persistence.models.animal import AnimalModel
from app.infrastructure.persistence.models.animal_event import AnimalEvent
from app.infrastructure.persistence.models.animal_movement import AnimalMovement
from app.infrastructure.persistence.models.batch import Batch
from app.infrastructure.persistence.models.batch_movement import BatchMovement
from app.infrastructure.persistence.models.cpf import CPF
from app.infrastructure.persistence.models.death_record import DeathRecord
from app.infrastructure.persistence.models.email_verification_code import (
    EmailVerificationCode,
)
from app.infrastructure.persistence.models.health import HealthModel
from app.infrastructure.persistence.models.owner import Owner
from app.infrastructure.persistence.models.owner_module import OwnerModule
from app.infrastructure.persistence.models.password_reset_token import PasswordResetToken
from app.infrastructure.persistence.models.paddock import Paddock, PaddockeStatus
from app.infrastructure.persistence.models.pasture import Pasture
from app.infrastructure.persistence.models.property import Property
from app.infrastructure.persistence.models.protocol import Protocol
from app.infrastructure.persistence.models.reproduction import Reproduction
from app.infrastructure.persistence.models.step import Step
from app.infrastructure.persistence.models.step_execution import StepExecution
from app.infrastructure.persistence.models.user import User
from app.infrastructure.persistence.models.weighing import Weighing

__all__ = [
    "Address",
    "AnimalModel",
    "AnimalEvent",
    "AnimalMovement",
    "Batch",
    "BatchMovement",
    "CPF",
    "DeathRecord",
    "EmailVerificationCode",
    "HealthModel",
    "Owner",
    "OwnerModule",
    "PasswordResetToken",
    "Paddock",
    "PaddockeStatus",
    "Pasture",
    "Property",
    "Protocol",
    "Reproduction",
    "Step",
    "StepExecution",
    "User",
    "Weighing",
]
