---
title: "Runbook: Migration Failure"
type: how-to
status: planned
owner: operations
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Runbook: Migration Failure

## Detectar

Comando de migração falha, schema fica em versão inesperada ou aplicação não inicia.

## Conter e diagnosticar

1. Interromper novas implantações e registrar versão aplicada.
2. Não editar tabela de versão manualmente sem plano revisado.
3. Comparar schema real, migration esperada e backup prévio.
4. Aplicar downgrade somente se suportado e seguro; caso contrário restaurar em ambiente controlado.
5. Corrigir migration de forma compatível, testar em cópia e repetir.

## Verificar recuperação

Versão do schema coincide com release, upgrade é idempotente e testes de integração passam.

## Escalonar

Escalonar imediatamente em caso de vazamento entre propriedades, perda de dados, credencial exposta, indisponibilidade prolongada ou recuperação sem procedimento seguro. Registrar linha do tempo, impacto, causa confirmada e ação preventiva.
