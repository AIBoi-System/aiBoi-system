---
title: "Bounded Contexts"
type: explanation
status: active
owner: domain
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Bounded Contexts

## Objetivo

Separação semântica entre identidade, propriedade, inventário, áreas, sanidade, reprodução e operações.

## Especificação

Identidade autentica; Propriedades autoriza; Inventário mantém animais e lotes; Áreas mantém pastagens e piquetes; Sanidade e Reprodução registram eventos; Relatórios apenas leem projeções autorizadas.

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
