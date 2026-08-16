---
title: "ADR-004: Avaliação de PostgreSQL"
type: governance
status: deprecated
owner: data
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# ADR-004: Avaliação de PostgreSQL

- Estado: Substituída pela [ADR-007](ADR-007-supabase-postgresql.md)

## Contexto

Na data desta decisão, a estrutura solicitada previa PostgreSQL, enquanto código,
dependências e documentação operacional usavam MySQL/PyMySQL; os testes usavam
SQLite.

## Decisão histórica

Naquele momento, decidiu-se manter MySQL como banco operacional até existir
análise aprovada e plano de migração. Essa decisão não está mais vigente.

## Critérios para reavaliar

Necessidade comprovada de recursos específicos, desempenho medido, compatibilidade SQLAlchemy, custo operacional, estratégia de backup, migração de dados, downtime e rollback.

## Consequências

Modelos devem evitar dependência desnecessária de extensões exclusivas. Uma migração futura exige ADR substituto, prova técnica, ambiente de homologação, dupla validação de dados e atualização de compose, drivers e runbooks.

## Substituição

Em 2026-07-27 foi aprovada a migração para PostgreSQL gerenciado pelo Supabase.
O contexto histórico desta decisão permanece preservado; a decisão vigente está
na ADR-007.
