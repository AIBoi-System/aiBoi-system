from app.domain.animal.entity import Animal
from app.presentation.schemas.animal import AnimalResponse


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
