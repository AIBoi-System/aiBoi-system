---
title: "Migrations"
type: reference
status: active
owner: data
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Migrations

## Objetivo

Estratégia obrigatória de alterações versionadas do schema.

## Especificação

Alembic é a autoridade de evolução do schema. `Base.metadata.create_all` não é
executado pela API. A migration inicial está em `backend/alembic/versions/`.

## Estado atual

Migration inicial `fdae6f06aeb9` validada contra `Base.metadata`, aplicada no
PostgreSQL local em 2026-08-14 e verificada com `alembic check` sem divergências.
A aplicação em ambiente gerenciado exige validação separada.

## Controles e regras

- Toda relação operacional preserva o tenant.
- Mudança de schema usa migração versionada.
- Transações fazem rollback em qualquer falha.
- Dados sensíveis possuem classificação e retenção.
- Migration aplicada nunca é reescrita.
- `MIGRATION_DATABASE_URL` usa conexão direta ou Supavisor sessão.
- Downgrade destrutivo exige autorização e backup restaurável.

## Comandos

```bash
cd backend
python -m alembic -c alembic.ini current
python -m alembic -c alembic.ini upgrade head
python -m alembic -c alembic.ini check
```

Para revisar SQL sem conectar:

```bash
python -m alembic -c alembic.ini upgrade head --sql
```

## Verificação

- Testar caminho válido, entrada inválida e falha de dependência.
- Testar acesso sem credencial, com papel insuficiente e entre propriedades quando aplicável.
- Verificar rollback e ausência de dados sensíveis em resposta e log.
- Comparar documentação, schema executável e comportamento observado.

## Referências

- [Database Overview](database-overview.md)
- [Tables](tables.md)
- [Invariants](../03-domain/invariants.md)
- [ADR-007](../04-architecture/adr/ADR-007-supabase-postgresql.md)
