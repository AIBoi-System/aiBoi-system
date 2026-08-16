---
title: "Exemplo de entidade"
type: tutorial
status: active
owner: backend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Exemplo de entidade

```python
@dataclass
class Animal:
    id: int | None
    property_id: int
    identification_number: IdentificationNumber

    @classmethod
    def create(cls, property_id: int, identification_number: int) -> "Animal":
        return cls(
            id=None,
            property_id=property_id,
            identification_number=IdentificationNumber(identification_number),
        )
```

A entidade protege invariantes e não importa Pydantic, FastAPI ou SQLAlchemy. Identidade técnica opcional diferencia novo objeto de objeto persistido.
