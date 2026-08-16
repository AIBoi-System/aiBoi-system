---
title: "Exemplo de router"
type: tutorial
status: active
owner: backend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Exemplo de router

```python
@router.get("/{animal_id}", response_model=AnimalResponse)
def get_animal(
    animal_id: int,
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    use_case: GetAnimalUseCase = Depends(get_get_animal_use_case),
):
    verify_property_access(db, property_id, current_user.id_user)
    return animal_to_response(use_case.execute(animal_id, property_id))
```

O router valida contrato e acesso, chama um caso de uso e converte resposta. Regra zootécnica, SQL e commit não pertencem ao router.
