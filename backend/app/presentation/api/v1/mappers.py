from app.modules.inventory.domain.entity import Animal
from app.modules.health.domain.entity import HealthRecord
from app.presentation.schemas.animal import AnimalResponse
from app.presentation.schemas.health.health_response import HealthResponse


def animal_to_response(animal: Animal) -> AnimalResponse:
    return AnimalResponse(
        id_animal=animal.id,
        identification_number=animal.identification_number.value,
        chip_id=animal.chip_id,
        pedigree_po=animal.pedigree_po,
        name=animal.name,
        sex=animal.sex,
        breed=animal.breed,
        animal_size=animal.animal_size,
        animal_life_status=animal.animal_life_status,
        reproductive_status=animal.reproductive_status,
        animal_category=animal.animal_category,
        birth_date=animal.birth_date,
        origin=animal.origin,
        entry_date=animal.entry_date,
        exit_date=animal.exit_date,
        weaning_date=animal.weaning_date,
        weaning_weight=animal.weaning_weight.value if animal.weaning_weight else None,
        birth_weight=animal.birth_weight.value if animal.birth_weight else None,
        notes=animal.notes,
        batch_id=animal.batch_id,
    )


def health_to_response(record: HealthRecord) -> HealthResponse:
    return HealthResponse(
        id_health_record=record.id,
        health_type=record.health_type,
        product_name=record.product_name,
        application_date=record.application_date,
        responsible=record.responsible,
        dosage=record.dosage,
        unit_price=record.unit_price,
        notes=record.notes,
        property_id=record.property_id,
        animal_id=record.animal_id,
        batch_id=record.batch_id,
    )














































