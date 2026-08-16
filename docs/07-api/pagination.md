---
title: "Pagination"
type: reference
status: partial
owner: backend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Pagination

## Objetivo

Paginação obrigatória para coleções potencialmente grandes.

## Especificação

Parâmetros alvo: limit com teto, cursor ou offset documentado e ordenação estável. Resposta informa items e continuidade sem executar count caro automaticamente.

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
