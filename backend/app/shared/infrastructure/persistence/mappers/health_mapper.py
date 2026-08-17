from app.modules.health.domain.entity import HealthRecord
from app.modules.health.infrastructure.persistence.health import HealthModel


def to_domain(model: HealthModel) -> HealthRecord:
    return HealthRecord(
        id=model.id_health_record,
        health_type=model.health_type,
        product_name=model.product_name,
        application_date=model.application_date,
        responsible=model.responsible,
        dosage=model.dosage,
        unit_price=model.unit_price,
        notes=model.notes,
        property_id=model.property_id,
        animal_id=model.animal_id,
        batch_id=model.batch_id,
    )


def to_model(entity: HealthRecord) -> HealthModel:
    return HealthModel(
        id_health_record=entity.id,
        health_type=entity.health_type,
        product_name=entity.product_name,
        application_date=entity.application_date,
        responsible=entity.responsible,
        dosage=entity.dosage,
        unit_price=entity.unit_price,
        notes=entity.notes,
        property_id=entity.property_id,
        animal_id=entity.animal_id,
        batch_id=entity.batch_id,
    )









































