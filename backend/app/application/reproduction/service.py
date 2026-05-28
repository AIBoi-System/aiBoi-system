from fastapi import HTTPException
from datetime import date
from sqlalchemy.orm import Session

from app.application.owner_module.service import OwnerModuleService
from app.domain.enums.animal.animal_life_status import AnimalLifeStatus
from app.domain.enums.animal.animal_reproductive_status import AnimalReproductiveStatus
from app.domain.enums.animal.animal_sex import AnimalSex
from app.domain.enums.module.system_module import SystemModule
from app.domain.enums.reproduction.reproduction_result import ReproductionResult
from app.domain.enums.reproduction.reproduction_status import ReproductionStatus
from app.domain.enums.reproduction.reproduction_type import ReproductionType
from app.domain.enums.step.step_name import StepName
from app.domain.enums.step.step_status import StepStatus
from app.infrastructure.persistence.models.animal import AnimalModel
from app.infrastructure.persistence.models.protocol import Protocol
from app.infrastructure.persistence.models.reproduction import Reproduction
from app.infrastructure.persistence.models.step import Step
from app.infrastructure.persistence.models.step_execution import StepExecution


class ReproductionService:
    @staticmethod
    def _ensure_reproduction_preconditions(animal: AnimalModel):
        if animal.animal_life_status != AnimalLifeStatus.ACTIVE:
            raise HTTPException(
                status_code=400,
                detail="Only active animals can enter reproduction.",
            )
        if animal.sex != AnimalSex.F:
            raise HTTPException(
                status_code=400,
                detail="Only female animals can participate in reproduction.",
            )
        if animal.reproductive_status != AnimalReproductiveStatus.OPEN:
            raise HTTPException(
                status_code=400,
                detail="Animal must have OPEN reproductive status.",
            )

    @staticmethod
    def _ensure_module_for_protocol(
        db: Session,
        current_user,
        reproduction_type: ReproductionType,
    ):
        if (current_user.type or "").lower() == "admin":
            return

        if reproduction_type == ReproductionType.MONTA_NATURAL:
            return

        module_map = {
            ReproductionType.IATF: SystemModule.IATF,
            ReproductionType.TE: SystemModule.TE,
            ReproductionType.FIV: SystemModule.FIV,
        }
        required_module = module_map.get(reproduction_type)
        if required_module:
            OwnerModuleService.ensure_owner_has_module(
                db, current_user.id_user, required_module
            )

    @staticmethod
    def _ensure_step_sequence(db: Session, reproduction_id: int, step: Step):
        if step.step_name == StepName.ZERO:
            return

        executions = ReproductionService.list_executions_by_reproduction(db, reproduction_id)
        completed_names = {
            ex.step.step_name
            for ex in executions
            if ex.status == StepStatus.COMPLETED and ex.step is not None
        }

        if step.step_name == StepName.EIGHT and StepName.ZERO not in completed_names:
            raise HTTPException(
                status_code=400,
                detail="Day 8 requires Day 0 to be completed.",
            )
        if step.step_name == StepName.TEN and StepName.EIGHT not in completed_names:
            raise HTTPException(
                status_code=400,
                detail="Day 10/17 requires Day 8 to be completed.",
            )
        if step.step_name == StepName.DIAGNOSIS and StepName.TEN not in completed_names:
            raise HTTPException(
                status_code=400,
                detail="Diagnosis requires Day 10/17 to be completed.",
            )

    @staticmethod
    def create_reproduction(db: Session, data, current_user):
        animal = db.query(AnimalModel).filter(AnimalModel.id_animal == data.animal_id).first()
        if not animal:
            raise HTTPException(status_code=404, detail="Animal not found.")
        ReproductionService._ensure_reproduction_preconditions(animal)
        ReproductionService._ensure_module_for_protocol(
            db, current_user, data.reproduction_type
        )

        if data.protocol_id:
            protocol = db.query(Protocol).filter(Protocol.id == data.protocol_id).first()
            if not protocol:
                raise HTTPException(status_code=404, detail="Protocol not found.")

        reproduction = Reproduction(**data.model_dump())
        db.add(reproduction)
        animal.reproductive_status = AnimalReproductiveStatus.BREEDING_READY
        db.commit()
        db.refresh(reproduction)
        return reproduction

    @staticmethod
    def list_reproductions(db: Session):
        return db.query(Reproduction).all()

    @staticmethod
    def get_reproduction(db: Session, reproduction_id: int):
        reproduction = (
            db.query(Reproduction).filter(Reproduction.id == reproduction_id).first()
        )
        if not reproduction:
            raise HTTPException(status_code=404, detail="Reproduction not found.")
        return reproduction

    @staticmethod
    def update_reproduction(db: Session, reproduction_id: int, data):
        reproduction = ReproductionService.get_reproduction(db, reproduction_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(reproduction, key, value)
        db.commit()
        db.refresh(reproduction)
        return reproduction

    @staticmethod
    def delete_reproduction(db: Session, reproduction_id: int):
        reproduction = ReproductionService.get_reproduction(db, reproduction_id)
        db.delete(reproduction)
        db.commit()

    @staticmethod
    def create_protocol(db: Session, data):
        protocol = Protocol(**data.model_dump())
        db.add(protocol)
        db.commit()
        db.refresh(protocol)
        return protocol

    @staticmethod
    def list_protocols(db: Session):
        return db.query(Protocol).all()

    @staticmethod
    def get_protocol(db: Session, protocol_id: int):
        protocol = db.query(Protocol).filter(Protocol.id == protocol_id).first()
        if not protocol:
            raise HTTPException(status_code=404, detail="Protocol not found.")
        return protocol

    @staticmethod
    def create_step(db: Session, protocol_id: int, data):
        ReproductionService.get_protocol(db, protocol_id)
        step_data = data.model_dump()
        step_data["protocol_id"] = protocol_id
        step = Step(**step_data)
        db.add(step)
        db.commit()
        db.refresh(step)
        return step

    @staticmethod
    def list_steps_by_protocol(db: Session, protocol_id: int):
        ReproductionService.get_protocol(db, protocol_id)
        return db.query(Step).filter(Step.protocol_id == protocol_id).all()

    @staticmethod
    def create_step_execution(db: Session, reproduction_id: int, data):
        reproduction = ReproductionService.get_reproduction(db, reproduction_id)
        step = db.query(Step).filter(Step.id == data.step_id).first()
        if not step:
            raise HTTPException(status_code=404, detail="Step not found.")

        if reproduction.protocol_id and step.protocol_id != reproduction.protocol_id:
            raise HTTPException(
                status_code=400,
                detail="This step does not belong to the reproduction protocol.",
            )
        ReproductionService._ensure_step_sequence(db, reproduction_id, step)

        payload = data.model_dump()
        payload["reproduction_id"] = reproduction_id
        execution = StepExecution(**payload)
        db.add(execution)

        if step.step_name == StepName.DIAGNOSIS:
            if not payload.get("execution_date"):
                raise HTTPException(
                    status_code=400,
                    detail="Diagnosis date is required.",
                )
            if payload["execution_date"] < reproduction.start_date:
                raise HTTPException(
                    status_code=400,
                    detail="Diagnosis date cannot be earlier than start date.",
                )
            reproduction.diagnosis_date = payload["execution_date"]
            if payload.get("result"):
                if payload["result"].value == "prenha":
                    reproduction.result = ReproductionResult.PREGNANT
                    reproduction.reproduction_status = ReproductionStatus.COMPLETED
                    reproduction.animal.reproductive_status = AnimalReproductiveStatus.PREGNANT
                elif payload["result"].value == "vazia":
                    reproduction.result = ReproductionResult.FAILED
                    reproduction.reproduction_status = ReproductionStatus.COMPLETED
                    reproduction.animal.reproductive_status = AnimalReproductiveStatus.OPEN

        db.commit()
        db.refresh(execution)
        return execution

    @staticmethod
    def list_executions_by_reproduction(db: Session, reproduction_id: int):
        ReproductionService.get_reproduction(db, reproduction_id)
        return (
            db.query(StepExecution)
            .filter(StepExecution.reproduction_id == reproduction_id)
            .all()
        )

    @staticmethod
    def register_birth(db: Session, reproduction_id: int, data):
        reproduction = ReproductionService.get_reproduction(db, reproduction_id)
        if data.birth_date > date.today():
            raise HTTPException(
                status_code=400,
                detail="Birth date cannot be in the future.",
            )

        allowed_categories = {"Novilho", "Novilha", "Bezerro", "Bezerra"}
        if data.calf_category not in allowed_categories:
            raise HTTPException(
                status_code=400,
                detail="Invalid calf category. Use Novilho(a) or Bezerro(a).",
            )

        reproduction.end_date = data.birth_date
        reproduction.reproduction_status = ReproductionStatus.COMPLETED
        reproduction.animal.reproductive_status = AnimalReproductiveStatus.OPEN
        merged_notes = (reproduction.notes or "") + (
            f"\nBirth registered at {data.birth_date.isoformat()} | "
            f"Alive calf: {data.calf_alive} | Sex: {data.calf_sex} | "
            f"Category: {data.calf_category} | Notes: {data.notes or '-'}"
        )
        reproduction.notes = merged_notes.strip()
        db.commit()
        db.refresh(reproduction)
        return reproduction

