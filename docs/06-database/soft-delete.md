---
title: "Soft Delete"
type: reference
status: planned
owner: data
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Soft Delete

## Objetivo

Política planejada para preservar histórico ao remover entidades relevantes.

## Especificação

Esta especificação define limites, dados envolvidos, controles obrigatórios, comportamento de falha e evidências necessárias para soft delete.

## Estado atual

Planejado; não há fluxo completo comprovado. Os controles descritos são requisitos para implementação futura.

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
