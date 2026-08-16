---
title: "ADR-005: API REST"
type: governance
status: active
owner: backend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# ADR-005: API REST

- Estado: Aceita

## Contexto

O aplicativo precisa de contrato simples sobre HTTP, compatível com Flutter, ferramentas comuns e documentação automática.

## Decisão

Expor recursos por API REST JSON com OpenAPI. Métodos e status seguem semântica HTTP; autenticação usa Bearer JWT; tenant é validado no servidor.

## Alternativas

GraphQL permitiria seleção flexível, mas aumentaria complexidade de autorização e caching. gRPC favoreceria comunicação interna tipada, porém não traz benefício suficiente ao cliente atual.

## Consequências

Mudanças incompatíveis exigem versão e migração. Coleções precisam de paginação. OpenAPI deve ser testável e exemplos Markdown não podem divergir do schema.
