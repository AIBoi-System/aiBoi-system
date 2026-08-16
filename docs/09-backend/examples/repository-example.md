---
title: "Exemplo de repository"
type: tutorial
status: active
owner: backend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Exemplo de repository

```python
class AnimalRepository(Protocol):
    def get_by_id(self, animal_id: int, property_id: int) -> Animal | None: ...
    def save(self, animal: Animal) -> Animal: ...
```

```python
def get_by_id(self, animal_id: int, property_id: int) -> Animal | None:
    model = (
        self._session.query(AnimalModel)
        .filter(
            AnimalModel.id_animal == animal_id,
            AnimalModel.property_id == property_id,
        )
        .first()
    )
    return to_domain(model) if model else None
```

Toda consulta operacional recebe tenant. O repository não decide autorização do usuário e não deve fazer commit isolado quando participa de transação maior.
