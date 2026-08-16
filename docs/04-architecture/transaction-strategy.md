---
title: "Transaction Strategy"
type: explanation
status: partial
owner: engineering
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Transaction Strategy

## Objetivo

Definição de limites de transação, commit, rollback e unidade de trabalho.

## Especificação

Um caso de uso que altera múltiplas tabelas deve confirmar tudo em uma transação. Repositories não devem decidir commits isolados quando participam da mesma operação.

## Estado no AiBoi

Há decisões e componentes implementados, mas a aderência é parcial devido à convivência entre arquitetura alvo e módulos legados.

## Regras

- Domínio não depende de FastAPI ou SQLAlchemy.
- Apresentação depende de casos de uso, não de modelos ORM.
- Migração arquitetural deve ser incremental e coberta por testes.

## Critérios de aceite documental

- O conceito possui limites e termos inequívocos.
- Estado atual e estado desejado estão separados.
- Exceções e cenários de falha estão registrados.
- Requisitos, testes e fontes relacionadas podem ser localizados.

## Referências

- [Current Architecture](current-architecture.md)
- [Backend Overview](../09-backend/backend-overview.md)
- [Frontend Overview](../08-frontend/frontend-overview.md)
