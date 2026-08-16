---
title: "Transactions"
type: reference
status: partial
owner: data
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Transactions

## Objetivo

Atomicidade, commit, rollback, concorrência e consistência.

## Especificação

A camada de aplicação delimita a transação. Repositories fazem add/flush e não commit independente quando um caso de uso envolve múltiplas gravações.

## Estado atual

Parcial. Existem componentes relacionados, mas a revisão do repositório encontrou lacunas que impedem considerar o tema concluído.

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
