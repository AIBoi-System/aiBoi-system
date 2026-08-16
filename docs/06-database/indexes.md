---
title: "Indexes"
type: reference
status: partial
owner: data
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Indexes

## Objetivo

Índices necessários para chaves, tenant, buscas e ordenações frequentes.

## Especificação

Indexar foreign keys e filtros recorrentes. Animais precisam de unicidade composta (property_id, identification_number), não unicidade global. Medir antes de criar índices redundantes.

## Estado atual

Parcial. A auditoria local encontrou 46 índices declarados no metadata; o
PostgreSQL reflete 52 porque 6 índices representam constraints de unicidade. Oito
foreign keys não possuem um índice dedicado com as mesmas colunas como prefixo.
Isso não causa drift nem quebra de integridade, mas joins e exclusões nas tabelas
afetadas devem ser medidos antes de propor uma migration de índices, evitando
índices redundantes.

## Controles e regras

- Toda relação operacional preserva o tenant.
- Mudança de schema usa migração versionada.
- Transações fazem rollback em qualquer falha.
- Dados sensíveis possuem classificação e retenção.

## Verificação

- Testar caminho válido, entrada inválida e falha de dependência.
- Testar acesso sem credencial, com papel insuficiente e entre propriedades quando aplicável.
- Verificar rollback e ausência de dados sensíveis em resposta e log.
- Comparar documentação, schema executável e comportamento observado.

## Referências

- [Database Overview](database-overview.md)
- [Tables](tables.md)
- [Invariants](../03-domain/invariants.md)
