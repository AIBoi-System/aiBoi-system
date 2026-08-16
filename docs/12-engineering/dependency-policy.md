---
title: "Dependency Policy"
type: reference
status: active
owner: engineering
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Dependency Policy

## Objetivo

Critérios de inclusão, atualização, pinning, licença e vulnerabilidade.

## Especificação

Evitar intervalos ilimitados em produção. Registrar motivo, licença e risco. Atualizações passam por testes; vulnerabilidade crítica exige correção ou mitigação documentada.

## Estado atual

Norma vigente para novas alterações e releases.

## Regras

- Mudança pequena e rastreável.
- Revisão proporcional ao risco.
- Código, teste e documentação evoluem juntos.
- Segurança e isolamento não podem ser dispensados.

## Critérios de verificação

- Comportamento principal e falhas possuem passos reproduzíveis.
- Entradas, saídas, dependências e responsáveis estão explícitos.
- Segurança, tenant e dados sensíveis foram avaliados.
- Testes e documentação são atualizados na mesma alteração.

## Referências

- [README](README.md)
- [DOCUMENTATION GUIDE](../DOCUMENTATION-GUIDE.md)
- [Release Checklist](../10-quality/release-checklist.md)
