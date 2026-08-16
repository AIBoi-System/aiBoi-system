---
title: "Multi Tenancy"
type: reference
status: partial
owner: data
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Multi Tenancy

## Objetivo

Representação e aplicação do property_id como fronteira de tenant.

## Especificação

property_id deve existir ou ser derivável de forma inequívoca para toda tabela operacional. Índices iniciam por property_id nas consultas mais frequentes.

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
