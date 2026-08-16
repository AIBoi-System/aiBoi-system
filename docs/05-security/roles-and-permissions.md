---
title: "Roles And Permissions"
type: reference
status: partial
owner: security
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Roles And Permissions

## Objetivo

Papéis, capacidades e política de menor privilégio.

## Especificação

O papel limita capacidades globais e não substitui ownership. O catálogo global
de protocolos reprodutivos e etapas pode ser consultado por usuário autenticado,
mas qualquer escrita é exclusiva de `admin`. Eventos, execuções e nascimentos
continuam subordinados ao vínculo com a propriedade.

## Estado atual

Parcial. Existem componentes relacionados, mas a revisão do repositório encontrou lacunas que impedem considerar o tema concluído.

## Controles e regras

- Negar por padrão e aplicar menor privilégio.
- Validar autorização no backend e por recurso.
- Nunca registrar ou retornar segredo, senha, token ou CPF completo.
- Falhas entre tenants são bloqueadoras de release.
- Criação ou alteração do catálogo global por papel diferente de `admin` retorna
  `403` e não produz escrita parcial.

## Verificação

- Testar caminho válido, entrada inválida e falha de dependência.
- Testar acesso sem credencial, com papel insuficiente e entre propriedades quando aplicável.
- Verificar rollback e ausência de dados sensíveis em resposta e log.
- Comparar documentação, schema executável e comportamento observado.

## Referências

- [Security Overview](security-overview.md)
- [Security Checklist](security-checklist.md)
- [Business Rules](../02-mvp/business-rules.md)
