---
title: "Modulo: Activities"
type: governance
status: planned
owner: domain
canonical: true
ai_index: true
last_verified: 2026-07-16
---
# Modulo: Activities

> Requisito: RF021  
> Estado: Planejado

## Responsabilidade

Catalogo de atividades do manejo. O modulo deve operar exclusivamente no contexto de uma propriedade autorizada, exceto identidade e administracao global explicitamente documentadas.

## Fluxos

- Criar ou registrar dados validos.
- Listar somente recursos acessiveis ao usuario atual.
- Consultar por identificador composto com a propriedade.
- Atualizar preservando invariantes e historico.
- Encerrar, arquivar ou excluir conforme a politica do dominio.

## Regras obrigatorias

1. O backend valida propriedade, papel e vinculo do recurso.
2. IDs recebidos do cliente nunca constituem autorizacao.
3. Operacoes invalidas retornam erro de dominio previsivel.
4. Dados sensiveis nao aparecem em logs nem respostas.
5. O fluxo possui testes de acesso entre propriedades.

## Estado e lacunas

Nao existe entrega funcional completa. Requer refinamento, criterios de aceite e decisao de persistencia antes da implementacao.

## Dependencias

- [Seguranca](../../05-security/README.md)
- [API](../../07-api/README.md)
- [Dominio](../../03-domain/README.md)
- [Cenarios de teste](../../02-mvp/test-scenarios.md)
