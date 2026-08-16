---
title: "Visão geral do banco de dados"
type: reference
status: active
owner: data
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Visão geral do banco de dados

## Objetivo

Visão da persistência SQLAlchemy em PostgreSQL.

## Especificação

O banco vigente é PostgreSQL, local no desenvolvimento e compatível com uma
implantação gerenciada futura. SQLAlchemy permanece como ORM e Alembic é a fonte
executável do schema. SQLite permanece apenas para testes rápidos; uma suíte
PostgreSQL é obrigatória antes do release.

## Estado atual

PostgreSQL 18 local está configurado com psycopg 3. A revisão Alembic
`fdae6f06aeb9` foi aplicada: as 21 tabelas da aplicação estão vazias e não há
divergência entre o catálogo PostgreSQL e `Base.metadata`. Os testes de integração
e isolamento ainda são necessários antes de declarar todos os CRUDs validados.
O reader não possui escrita em tabelas ou sequências, mas a auditoria encontrou
`TEMPORARY` ainda herdado de `PUBLIC`; o configurador foi corrigido e precisa ser
reexecutado com o administrador `postgres` para efetivar a revogação no banco.

## Controles e regras

- Toda relação operacional preserva o tenant.
- Mudança de schema usa migração versionada.
- Transações fazem rollback em qualquer falha.
- Dados sensíveis possuem classificação e retenção.
- O startup da API nunca cria ou altera tabelas.
- Runtime usa `DATABASE_URL`; Alembic pode usar `MIGRATION_DATABASE_URL`.
- Conexões e erros nunca expõem credenciais.
- Tabelas expostas pela Data API usam RLS antes de grants.
- O papel `codex_reader` recebe somente conexão, uso do schema e `SELECT`; o
  configurador revoga `CONNECT` e `TEMPORARY` herdados de `PUBLIC` antes de aplicar
  grants explícitos.

## Verificação

- Testar caminho válido, entrada inválida e falha de dependência.
- Testar acesso sem credencial, com papel insuficiente e entre propriedades quando aplicável.
- Verificar rollback e ausência de dados sensíveis em resposta e log.
- Comparar documentação, schema executável e comportamento observado.
- Executar `python -m alembic -c alembic.ini upgrade head`.
- Executar testes reais contra PostgreSQL antes do release.

## Referências

- [Database Overview](database-overview.md)
- [Tables](tables.md)
- [Invariants](../03-domain/invariants.md)
- [ADR-007](../04-architecture/adr/ADR-007-supabase-postgresql.md)
- [Migrations](migrations.md)
