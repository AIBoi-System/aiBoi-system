---
title: "Runbook: Mobile Build Failure"
type: how-to
status: planned
owner: operations
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Runbook: Mobile Build Failure

## Detectar

flutter analyze, testes, Gradle ou assinatura Android falham.

## Conter e diagnosticar

1. Registrar Flutter/Dart, JDK, Gradle, Android SDK e mensagem completa.
2. Executar flutter doctor e confirmar dependências sem atualizar tudo automaticamente.
3. Separar falha de análise, teste, compilação, recurso e assinatura.
4. Limpar artefatos somente depois de preservar evidência; restaurar dependências pelo lockfile.
5. Validar configuração de assinatura fora do Git e repetir build reproduzível.

## Verificar recuperação

flutter analyze e flutter test passam; APK/AAB instala, inicia e aponta para ambiente correto.

## Escalonar

Escalonar imediatamente em caso de vazamento entre propriedades, perda de dados, credencial exposta, indisponibilidade prolongada ou recuperação sem procedimento seguro. Registrar linha do tempo, impacto, causa confirmada e ação preventiva.
