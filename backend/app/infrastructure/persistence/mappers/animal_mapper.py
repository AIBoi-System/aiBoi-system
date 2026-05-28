from app.domain.animal.entity import Animal
from app.infrastructure.persistence.models.animal import AnimalModel


def to_domain(model: AnimalModel) -> Animal:
    return Animal(
        id_animal=model.id_animal,
        identification_number=model.identification_number,
        chip_id=model.chip_id,
        pedigree_po=model.pedigree_po,
        name=model.name,
        sex=model.sex,
        breed=model.breed,
        animal_size=model.animal_size,
        animal_life_status=model.animal_life_status,
        reproductive_status=model.reproductive_status,
        animal_category=model.animal_category,
        birth_date=model.birth_date,
        origin=model.origin,
        entry_date=model.entry_date,
        exit_date=model.exit_date,
        weaning_date=model.weaning_date,
        weaning_weight=model.weaning_weight,
        birth_weight=model.birth_weight,
        notes=model.notes,
        batch_id=model.batch_id,
    )


def to_model(entity: Animal) -> AnimalModel:
    return AnimalModel(
        id_animal=entity.id_animal,
        identification_number=entity.identification_number,
        chip_id=entity.chip_id,
        pedigree_po=entity.pedigree_po,
        name=entity.name,
        sex=entity.sex,
        breed=entity.breed,
        animal_size=entity.animal_size,
        animal_life_status=entity.animal_life_status,
        reproductive_status=entity.reproductive_status,
        animal_category=entity.animal_category,
        birth_date=entity.birth_date,
        origin=entity.origin,
        entry_date=entity.entry_date,
        exit_date=entity.exit_date,
        weaning_date=entity.weaning_date,
        weaning_weight=entity.weaning_weight,
        birth_weight=entity.birth_weight,
        notes=entity.notes,
        batch_id=entity.batch_id,
    )
