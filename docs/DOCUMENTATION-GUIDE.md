---
title: "Guia de documentacao"
type: how-to
status: active
owner: documentation
canonical: true
ai_index: true
last_verified: 2026-07-16
---
# Guia de documentacao

## Principios

- Escrever em portugues do Brasil, com linguagem objetiva.
- Separar estado atual de estado desejado.
- Nao registrar segredo, credencial, CPF real ou dado pessoal.
- Usar identificadores estaveis: RF, RN, UC, ADR e CT.
- Referenciar a regra proprietaria em vez de copiar o mesmo texto.

## Fluxo de alteracao

1. Identificar documentos afetados.
2. Atualizar requisito, regra ou decisao proprietaria.
3. Atualizar contratos tecnicos e cenarios de teste.
4. Conferir links relativos.
5. Registrar a mudanca no `CHANGELOG.md`.

## Metadados minimos

Cada especificacao deve informar objetivo, estado, regras, criterios de verificacao e referencias. Funcionalidades nao implementadas devem usar o estado **Planejado**. O front matter obrigatorio segue o [esquema de metadados](METADATA-SCHEMA.md).

## Tipos Diataxis

- `tutorial`: conduz aprendizado completo e verificavel.
- `how-to`: resolve uma tarefa concreta.
- `reference`: descreve contrato, campo, endpoint ou regra para consulta.
- `explanation`: apresenta contexto, alternativas e razoes.
- `governance`: controla processo, precedencia ou decisao.

Nao crie uma pagina apenas para preencher a arvore. Use `status: draft`, `canonical: false` e `ai_index: false` ate existir conteudo e evidencia suficientes.

## Nomes

Arquivos usam `kebab-case.md`. Pastas numeradas representam a ordem de leitura. Termos centrais seguem o [glossario](01-product/glossary.md).
