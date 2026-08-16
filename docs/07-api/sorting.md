---
title: "Sorting"
type: reference
status: partial
owner: backend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Sorting

## Objetivo

Ordenação permitida, padrão estável e proteção contra campos arbitrários.

## Especificação

Esta especificação define limites, dados envolvidos, controles obrigatórios, comportamento de falha e evidências necessárias para sorting.

## Estado atual

Parcial. Existem componentes relacionados, mas a revisão do repositório encontrou lacunas que impedem considerar o tema concluído.

## Controles e regras

- Schemas validam toda entrada e saída.
- Rotas privadas exigem autenticação, autorização e tenant.
- Erros não expõem implementação.
- Coleções usam paginação quando crescerem.

## Verificação

- Testar caminho válido, entrada inválida e falha de dependência.
- Testar acesso sem credencial, com papel insuficiente e entre propriedades quando aplicável.
- Verificar rollback e ausência de dados sensíveis em resposta e log.
- Comparar documentação, schema executável e comportamento observado.

## Referências

- [Api Overview](api-overview.md)
- [Animals](endpoints/animals.md)
- [Api Security](../05-security/api-security.md)
