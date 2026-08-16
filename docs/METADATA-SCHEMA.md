---
title: Esquema de metadados da documentacao
type: reference
status: active
owner: documentation
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Esquema de metadados

Todo Markdown oficial, exceto fontes historicas brutas, deve iniciar com front matter YAML.

| Campo | Valores | Finalidade |
|---|---|---|
| `title` | texto | Titulo unico e pesquisavel |
| `type` | tutorial, how-to, reference, explanation, governance, archive | Necessidade Diataxis |
| `status` | active, partial, planned, draft, deprecated, archived | Confiabilidade atual |
| `owner` | product, domain, backend, frontend, security, data, quality, operations, engineering, documentation | Responsavel pela revisao |
| `canonical` | true ou false | Define fonte de verdade |
| `ai_index` | true ou false | Autoriza inclusao no corpus interno |
| `last_verified` | AAAA-MM-DD | Ultima comparacao com fontes reais |
| `source_paths` | lista opcional | Codigo ou contrato que sustenta a pagina |
| `requirements` | lista opcional | RF, RN, RNF ou ADR relacionados |

`ai_index` nao substitui controle de acesso. Conteudo sensivel exige autorizacao no mecanismo de recuperacao.
