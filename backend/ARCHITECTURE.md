# Arquitetura AiBoi — Clean Architecture + DDD

```
backend/app/
├── domain/              # Entidades, regras de negócio, portas (repositórios)
│   ├── animal/
│   ├── health/
│   ├── enums/
│   └── shared/
├── application/         # Casos de uso (orquestração)
│   ├── animal/use_cases.py
│   ├── health/use_cases.py
│   └── {modulo}/service.py   # serviços legados em migração
├── infrastructure/      # SQLAlchemy, repositórios concretos, segurança
│   ├── database/
│   └── persistence/
├── presentation/        # API FastAPI + schemas Pydantic
│   ├── api/v1/
│   └── schemas/
└── main.py
```

## Fluxo de uma requisição (ex.: Animal)

1. **Presentation** — `animal_router` valida JSON com Pydantic.
2. **Application** — `CreateAnimalUseCase` orquestra a operação.
3. **Domain** — `Animal.ensure_unique_identification()` aplica regra de negócio.
4. **Infrastructure** — `SqlAlchemyAnimalRepository` persiste via `AnimalModel`.

## Testes

```bash
cd backend
set DATABASE_URL=sqlite:///:memory:   # Windows
python -m pytest tests/ -v
```

Os testes usam SQLite em memória e não exigem MySQL.
