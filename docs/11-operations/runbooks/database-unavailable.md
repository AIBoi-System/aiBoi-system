---
title: "Runbook: Database Unavailable"
type: how-to
status: planned
owner: operations
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Runbook: Database Unavailable

## Detectar

API falha ao abrir conexão, health check do banco falha ou pool esgota.

## Conter e diagnosticar

1. Confirmar host, DNS, porta, TLS e credenciais sem imprimi-las.
2. Verificar disponibilidade, conexões, armazenamento e limites do banco.
3. Suspender migrações e gravações manuais durante diagnóstico.
4. Reiniciar apenas componentes comprovadamente travados; não recriar banco.
5. Acionar restauração somente diante de corrupção/perda confirmada e backup validado.

## Verificar recuperação

SELECT de saúde, login e operação transacional simples funcionam com rollback testado.

## Escalonar

Escalonar imediatamente em caso de vazamento entre propriedades, perda de dados, credencial exposta, indisponibilidade prolongada ou recuperação sem procedimento seguro. Registrar linha do tempo, impacto, causa confirmada e ação preventiva.
