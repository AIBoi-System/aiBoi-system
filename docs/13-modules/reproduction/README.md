---
title: "Modulo: Reproduction"
type: governance
status: partial
owner: domain
canonical: true
ai_index: true
last_verified: 2026-08-14
---
# Modulo: Reproduction

> Requisito: RF005  
> Estado: Parcial

## Responsabilidade

Eventos, protocolos e nascimento. O modulo deve operar exclusivamente no contexto de uma propriedade autorizada, exceto identidade e administracao global explicitamente documentadas.

Protocolos e etapas constituem catalogo global compartilhado. Usuarios
autenticados podem consulta-lo; somente admin pode criar ou modificar itens. As
execucoes de etapas e os eventos reprodutivos permanecem vinculados a propriedade.

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
6. Escrita no catalogo global exige papel admin e falha com `403` para outros papeis.

## Estado e lacunas

Existem componentes no codigo, mas faltam uniformidade arquitetural, isolamento, autorizacao ou testes para considerar o modulo concluido.

## Dependencias

- [Seguranca](../../05-security/README.md)
- [API](../../07-api/README.md)
- [Dominio](../../03-domain/README.md)
- [Cenarios de teste](../../02-mvp/test-scenarios.md)
