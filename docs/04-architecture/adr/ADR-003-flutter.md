---
title: "ADR-003: Flutter"
type: governance
status: active
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# ADR-003: Flutter

- Estado: Aceita

## Contexto

O produto prioriza Android, mas pode precisar de web e desktop. A equipe busca uma base única e interface adequada ao uso em campo.

## Decisão

Usar Flutter/Dart com Material 3. Android é plataforma prioritária do MVP; a presença de pastas para outros alvos não significa suporte homologado.

## Alternativas

Android nativo oferece integração direta, mas duplica esforço para outros alvos. React Native ampliaria uso de JavaScript, porém mudaria ferramentas e padrões já implementados.

## Consequências

Responsividade, acessibilidade e desempenho precisam ser testados por plataforma. Plugins nativos são avaliados antes de adoção. Features seguem arquitetura própria, e regras de autorização permanecem no backend.
