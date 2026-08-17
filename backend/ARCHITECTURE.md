# Arquitetura do backend AiBoi

O backend é um monólito modular FastAPI em migração incremental para DDD e
Clean Architecture. A especificação canônica de dependências está em
[`docs/04-architecture/dependency-rules.md`](../docs/04-architecture/dependency-rules.md).

## Estrutura vigente

```text
app/
|-- modules/
|   |-- inventory/{domain,application,infrastructure}
|   `-- health/{domain,application,infrastructure}
|-- shared/{domain,application,infrastructure}
|-- presentation/{api,schemas}
|-- infrastructure/       # adapters transversais
`-- main.py               # bootstrap FastAPI
```

Fluxo alvo:

```text
Router -> Use case -> Domain port <- Infrastructure adapter
```

O código legado pode seguir temporariamente `Router -> Service -> ORM`, mas não
deve ampliar os acoplamentos registrados. Os testes em
`tests/architecture/test_layer_dependencies.py` bloqueiam novas violações.

## Verificação

```powershell
cd backend
python -m pytest tests/architecture -q
python -m pytest tests/api -q
```

Testes locais usam SQLite em memória. A validação de release também deve
executar a integração PostgreSQL com schema aplicado por Alembic.
