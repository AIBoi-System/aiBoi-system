---
title: "Coding Standards"
type: reference
status: partial
owner: backend
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Coding Standards

## Objetivo

Regras Python de legibilidade, simplicidade, erros e manutenção.

## Padrão obrigatório para código novo

O backend segue PEP 8, DDD tático, SOLID e as regras de dependência do monólito
modular. Código legado pode ser migrado incrementalmente, mas uma alteração não
pode criar uma nova exceção arquitetural nem ampliar uma existente.

## Estado atual

O padrão está ativo e possui guardrails automatizados. A conformidade do legado
ainda é parcial; as exceções conhecidas estão congeladas em
`tests/architecture/test_layer_dependencies.py`.

## PEP 8 e legibilidade

- arquivos são UTF-8, usam LF, indentação de quatro espaços e newline final;
- classes usam `PascalCase`; funções, módulos e variáveis usam `snake_case`;
- constantes usam `UPPER_SNAKE_CASE`;
- imports ficam agrupados em biblioteca padrão, terceiros e aplicação;
- fronteiras públicas possuem type hints de parâmetros e retorno;
- o limite do projeto é 88 caracteres; expressões devem ser quebradas de forma
  legível, sem abreviações obscuras;
- não usar argumento mutável como valor padrão, `except Exception` silencioso,
  `print` em código de aplicação ou comentário que repete o código;
- funções devem ser pequenas e possuir uma responsabilidade observável.

O `.editorconfig` da raiz aplica charset, espaços, newline e whitespace nos
editores compatíveis. A adoção de um linter/formatter no CI exige dependência de
desenvolvimento aprovada e será registrada separadamente.

## SOLID no AiBoi

- **SRP:** router trata HTTP, caso de uso orquestra, entidade protege regra e
  repository persiste.
- **OCP:** novas integrações implementam portas; casos de uso não recebem
  condicionais específicas de fornecedor.
- **LSP:** adapters preservam o contrato da porta, inclusive erros, tenant e
  rollback.
- **ISP:** preferir portas pequenas por capacidade a repositories genéricos.
- **DIP:** application e domain dependem de abstrações; infraestrutura implementa
  essas abstrações e é ligada no composition root.

## DDD, persistência e API

- Domain não importa FastAPI, Pydantic ou SQLAlchemy.
- Routers não contêm regra de negócio nem executam consultas ORM.
- Resources operacionais usam `id + property_id` e validam o tenant no backend.
- Schemas de transporte não são entidades nem models ORM.
- Toda escrita possui limite transacional e rollback em falha.
- Mudança estrutural de banco exige migration Alembic e `alembic check` limpo.
- Respostas não expõem senha, token, CPF completo, SQL ou stack trace.

## Definição de pronto

Uma alteração backend só está pronta quando:

1. testes de domínio/aplicação cobrem regra e falha;
2. testes de API cobrem autenticação, validação e resposta;
3. recurso de propriedade possui teste cross-tenant com 404;
4. `pytest`, `compileall`, testes arquiteturais e `git diff --check` passam;
5. mudanças ORM possuem migration e teste PostgreSQL transacional;
6. OpenAPI e documentação canônica permanecem alinhados;
7. nenhuma credencial ou dado sensível foi adicionado ao repositório.

Comandos de release:

```powershell
cd backend
..\.venv\Scripts\python.exe -m pytest -q
$env:RUN_POSTGRES_INTEGRATION = "1"
..\.venv\Scripts\python.exe -m pytest -q
Remove-Item Env:RUN_POSTGRES_INTEGRATION
..\.venv\Scripts\python.exe -m alembic -c alembic.ini check
```

## Referências

- [Backend Overview](backend-overview.md)
- [Dependency Rules](../04-architecture/dependency-rules.md)
- [Tenant Isolation](../05-security/tenant-isolation.md)
- [Sequência das telas](../08-frontend/screen-implementation-sequence.md)
