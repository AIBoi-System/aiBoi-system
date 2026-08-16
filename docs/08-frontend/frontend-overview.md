---
title: "Visao do frontend"
type: explanation
status: partial
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-07-16
---
# Visao do frontend

Aplicativo Flutter com Material, `flutter_bloc` e cliente HTTP. A organizacao e feature-first.

## Features atuais

Autenticacao, cadastro em etapas, propriedade, home, dashboard, animais e atividades. Ha telas para lista, detalhe e cadastro de animais.

## Padroes

- `presentation`: paginas, widgets e Cubits.
- `domain`: entidades, contratos e casos de uso.
- `data`: datasources, models e repositories concretos.
- `core`: rede, tema, navegacao, DI e widgets compartilhados.

## Requisitos de experiencia

Prioridade Android, telas pequenas, baixa carga cognitiva, estados completos de loading/erro/vazio, validacao proxima ao campo e nenhuma autorizacao confiada apenas a interface.

## Lacunas

Nao existe suite de testes Flutter no repositorio e a estrategia offline ainda e planejada.
