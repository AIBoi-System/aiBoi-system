---
title: "Exemplo de caso de uso"
type: tutorial
status: active
owner: backend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Exemplo de caso de uso

```python
class GetAnimal:
    def __init__(self, repository: AnimalRepository) -> None:
        self._repository = repository

    def execute(self, animal_id: int, property_id: int) -> Animal:
        animal = self._repository.get_by_id(animal_id, property_id)
        if animal is None:
            raise EntityNotFoundError("Animal", animal_id)
        return animal
```

O caso de uso recebe apenas dados já autorizados pela boundary apropriada, coordena portas e lança exceção de aplicação. Não retorna ORM nem HTTPException.
