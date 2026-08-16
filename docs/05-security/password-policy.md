---
title: "Password Policy"
type: reference
status: partial
owner: security
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Password Policy

## Objetivo

Requisitos de criação, armazenamento, redefinição e proteção contra abuso de senhas.

## Especificação

Senha deve ter comprimento mínimo definido no schema, aceitar frases longas, ser armazenada com hash adaptativo e nunca truncada. Login e recuperação recebem rate limit. Redefinição invalida tokens anteriores.

## Estado atual

Parcial. Existem componentes relacionados, mas a revisão do repositório encontrou lacunas que impedem considerar o tema concluído.

## Controles e regras

- Negar por padrão e aplicar menor privilégio.
- Validar autorização no backend e por recurso.
- Nunca registrar ou retornar segredo, senha, token ou CPF completo.
- Falhas entre tenants são bloqueadoras de release.

## Verificação

- Testar caminho válido, entrada inválida e falha de dependência.
- Testar acesso sem credencial, com papel insuficiente e entre propriedades quando aplicável.
- Verificar rollback e ausência de dados sensíveis em resposta e log.
- Comparar documentação, schema executável e comportamento observado.

## Referências

- [Security Overview](security-overview.md)
- [Security Checklist](security-checklist.md)
- [Business Rules](../02-mvp/business-rules.md)
