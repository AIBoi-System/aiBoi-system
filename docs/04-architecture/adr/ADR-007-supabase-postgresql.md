---
title: "ADR-007: PostgreSQL gerenciado pelo Supabase"
type: governance
status: active
owner: data
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# ADR-007: PostgreSQL gerenciado pelo Supabase

- Estado: Aceita; PostgreSQL local configurado e migration `fdae6f06aeb9` aplicada
- Substitui: [ADR-004](ADR-004-postgresql.md)

## Contexto

O AiBoi usava MySQL/PyMySQL em produção e SQLite nos testes. A aplicação já
centralizava persistência em SQLAlchemy, sem tipos ou SQL específicos de MySQL,
mas criava tabelas com `Base.metadata.create_all` no startup e não possuía
migrations versionadas.

## Decisão

Adotar PostgreSQL, mantendo SQLAlchemy como ORM e Alembic como autoridade de
migrations. O desenvolvimento usa PostgreSQL local; Supabase permanece uma opção
de implantação gerenciada, sujeita a validação operacional própria.

- Driver: psycopg 3.
- Runtime local: conexão direta com PostgreSQL.
- Runtime gerenciado: conexão direta ou pooler em modo de sessão.
- Migrations e backup: conexão direta, configurada separadamente quando possível.
- Testes rápidos: SQLite permanece como camada unitária temporária.
- Testes de integração: PostgreSQL torna-se obrigatório antes do release.
- Isolamento: filtros por propriedade no backend permanecem obrigatórios.
- RLS: habilitar somente em tabelas expostas por uma Data API e junto de policies
  de ownership revisadas; o schema local não ativa RLS sem policies.

## Consequências

### Positivas

- migrations transacionais e schema versionado;
- recursos nativos de PostgreSQL e integração Supabase;
- melhor base para índices compostos, JSONB, observabilidade e RLS;
- eliminação da criação silenciosa de tabelas no startup.

### Custos e riscos

- uma origem legada, se identificada, exige plano separado de transferência e reconciliação;
- enums nativos precisam de lifecycle explícito nas migrations;
- SQLite não detecta diferenças importantes do PostgreSQL;
- conexão privilegiada do backend pode contornar RLS, portanto autorização ORM
  não pode ser removida.

## Critérios de conclusão

- migration inicial aplicada em banco PostgreSQL vazio;
- dados de origem, se existirem, reconciliados e sequences ajustadas;
- suíte PostgreSQL e testes cross-tenant verdes;
- verificações do provedor gerenciado sem bloqueadores, quando aplicável;
- backup, restauração e rollback ensaiados;
- documentação e segredos de ambiente atualizados.
