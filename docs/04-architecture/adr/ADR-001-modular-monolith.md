---
title: "ADR-001: Monólito modular"
type: governance
status: active
owner: engineering
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# ADR-001: Monólito modular

- Estado: Aceita como arquitetura alvo
- Data de consolidação: 2026-07-16

## Contexto

O AiBoi possui equipe e escopo de MVP incompatíveis com custo operacional de microserviços, mas os módulos de inventário, sanidade e reprodução precisam de limites claros.

## Decisão

Manter uma aplicação FastAPI implantável como unidade única, separada internamente por módulos, camadas e portas. Cada módulo possui linguagem, casos de uso e persistência identificáveis. Integração interna ocorre por chamadas de aplicação ou eventos de domínio, não por imports arbitrários de modelos ORM.

## Alternativas

- Monólito sem limites: mais rápido inicialmente, mas aumenta acoplamento já visível.
- Microserviços: isolamento operacional maior, porém adiciona rede, observabilidade, consistência distribuída e implantação prematuras.

## Consequências

Transações locais continuam simples. Limites precisam ser fiscalizados por revisão e testes. Um módulo somente será extraído quando houver necessidade comprovada de escala, autonomia ou isolamento operacional.
