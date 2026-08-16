---
title: "Arquitetura"
type: explanation
status: active
owner: engineering
canonical: true
ai_index: true
last_verified: 2026-07-16
---
# Arquitetura

> Estado: documento indice.

Esta secao organiza as decisoes e especificacoes de arquitetura do AiBoi. A fonte de verdade deve ser interpretada junto do [indice geral](../INDEX.md), da [especificacao mestra](../00-master/especificacao-completa-aiboi.md) e do codigo atual.

## Principios

- Distinguir claramente comportamento implementado, parcial e planejado.
- Evitar duplicar regras; referenciar o documento proprietario.
- Registrar mudancas relevantes no changelog e, quando necessario, em ADR.

## Conteudo

- [Architecture Overview](architecture-overview.md)
- [Current Architecture](current-architecture.md)
- [Target Architecture](target-architecture.md)
- [Modular Monolith](modular-monolith.md)
- [Backend Architecture](backend-architecture.md)
- [Frontend Architecture](frontend-architecture.md)
- [Dependency Rules](dependency-rules.md)
- [Module Boundaries](module-boundaries.md)
- [Integration Patterns](integration-patterns.md)
- [Transaction Strategy](transaction-strategy.md)
- [Error Handling](error-handling.md)
- [Logging Strategy](logging-strategy.md)
- [Caching Strategy](caching-strategy.md)
- [Offline Strategy](offline-strategy.md)
- [Synchronization Strategy](synchronization-strategy.md)
- [Scalability](scalability.md)
- [Technical Debt](technical-debt.md)
