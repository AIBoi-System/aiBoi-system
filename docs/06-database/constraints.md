---
title: "Constraints"
type: reference
status: partial
owner: data
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Constraints

## Objetivo

Restrições de nulidade, unicidade, domínio, referência e consistência.

## Especificação

O schema local possui 33 foreign keys e 6 constraints de unicidade, sem drift em
relação ao ORM. A identificação animal é única por
`(property_id, identification_number)`. Relações de animal/lote/pastagem usadas
por `animals`, `health_records` e `paddocks` possuem foreign keys compostas com
`property_id`.

## Estado atual

Parcial. Algumas tabelas operacionais derivam a propriedade por relacionamento,
em vez de armazenar `property_id`; por isso, os testes cross-tenant e os filtros
ORM continuam bloqueadores mesmo com as constraints atuais válidas.

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
