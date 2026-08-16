---
title: "Rate Limiting"
type: reference
status: partial
owner: backend
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Rate Limiting

## Objetivo

Proteção de endpoints sensíveis contra abuso e consumo excessivo.

## Especificação

Priorizar login, cadastro, verificação, recuperação, buscas e relatórios. Chave
combina IP e identidade quando disponível; `429` informa a janela sem revelar a
existência de conta.

- `ENV=production`: `REDIS_URL` é obrigatória e o Redis precisa estar alcançável
  no startup. O rate limiting é compartilhado entre processos e instâncias.
- Desenvolvimento e testes: na ausência de `REDIS_URL`, é permitido fallback em
  memória, limitado ao processo atual.
- Produção nunca degrada silenciosamente para memória; falha de configuração ou
  conectividade impede o startup.

## Estado atual

Contrato definido para Redis distribuído em produção e memória em desenvolvimento.
A conclusão depende dos testes de startup indisponível e concorrência entre instâncias.

## Controles e regras

- Schemas validam toda entrada e saída.
- Rotas privadas exigem autenticação, autorização e tenant.
- Erros não expõem implementação.
- Coleções usam paginação quando crescerem.
- Produção falha fechada quando o backend distribuído de rate limiting não está disponível.

## Verificação

- Testar caminho válido, entrada inválida e falha de dependência.
- Testar acesso sem credencial, com papel insuficiente e entre propriedades quando aplicável.
- Verificar rollback e ausência de dados sensíveis em resposta e log.
- Comparar documentação, schema executável e comportamento observado.

## Referências

- [Api Overview](api-overview.md)
- [Animals](endpoints/animals.md)
- [Api Security](../05-security/api-security.md)
