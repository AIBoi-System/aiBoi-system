---
title: "Domain Model Evolution"
type: explanation
status: active
owner: domain
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Domain Model Evolution

## Objetivo

Estratégia para evoluir o modelo sem quebrar invariantes, contratos ou histórico.

## Especificação

A especificação de domain model evolution deve manter definição, limites, decisões, exemplos válidos e casos de falha rastreáveis.

## Estado no AiBoi

Esta página define a direção vigente e deve ser confirmada contra código, testes e decisões aprovadas antes de cada release.

## Regras

- Usar a linguagem ubíqua.
- Preservar histórico e isolamento por propriedade.
- Manter regras de negócio fora de routers e widgets.

## Critérios de aceite documental

- O conceito possui limites e termos inequívocos.
- Estado atual e estado desejado estão separados.
- Exceções e cenários de falha estão registrados.
- Requisitos, testes e fontes relacionadas podem ser localizados.

## Referências

- [Business Rules](../02-mvp/business-rules.md)
- [README](../13-modules/README.md)
