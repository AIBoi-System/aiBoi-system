"""Modelos ORM — importados no bootstrap para create_all."""

from app.shared.infrastructure.persistence.address import Address
from app.modules.inventory.infrastructure.persistence.animal import AnimalModel
from app.shared.infrastructure.persistence.animal_event import AnimalEvent
from app.shared.infrastructure.persistence.animal_movement import AnimalMovement
from app.modules.inventory.infrastructure.persistence.batch import Batch
from app.shared.infrastructure.persistence.batch_movement import BatchMovement
from app.shared.infrastructure.persistence.cpf import CPF
from app.modules.inventory.infrastructure.persistence.death_record import DeathRecord
from app.shared.infrastructure.persistence.email_verification_code import (
    EmailVerificationCode,
)
from app.modules.health.infrastructure.persistence.health import HealthModel
from app.shared.infrastructure.persistence.owner import Owner
from app.shared.infrastructure.persistence.owner_module import OwnerModule
from app.shared.infrastructure.persistence.password_reset_token import PasswordResetToken
from app.shared.infrastructure.persistence.paddock import Paddock, PaddockeStatus
from app.shared.infrastructure.persistence.pasture import Pasture
from app.shared.infrastructure.persistence.property import Property
from app.shared.infrastructure.persistence.protocol import Protocol
from app.modules.inventory.infrastructure.persistence.reproduction import Reproduction
from app.shared.infrastructure.persistence.step import Step
from app.shared.infrastructure.persistence.step_execution import StepExecution
from app.shared.infrastructure.persistence.user import User
from app.modules.inventory.infrastructure.persistence.weighing import Weighing

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










































