---
title: "Endpoints de Reproduction"
type: reference
status: partial
owner: backend
canonical: true
ai_index: true
last_verified: 2026-08-14
source_paths:
  - backend/app/presentation/api/v1/reproduction_router.py
---

# Endpoints de Reproduction

| Metodo | Caminho | Protecao atual | Finalidade |
|---|---|---|---|
| POST | `/reproductions/` | Owner ou admin | Cria evento |
| GET | `/reproductions/` | JWT por papel | Lista eventos |
| GET | `/reproductions/{id}` | JWT por papel | Consulta evento |
| PUT | `/reproductions/{id}` | Owner ou admin | Atualiza evento |
| DELETE | `/reproductions/{id}` | Owner ou admin | Exclui evento |
| POST | `/reproductions/protocols` | Somente admin | Cria protocolo no catálogo global |
| GET | `/reproductions/protocols` | JWT por papel | Lista protocolos |
| GET | `/reproductions/protocols/{protocol_id}` | JWT por papel | Consulta protocolo global |
| POST | `/reproductions/protocols/{protocol_id}/steps` | Somente admin | Cria etapa no catálogo global |
| GET | `/reproductions/protocols/{protocol_id}/steps` | JWT por papel | Lista etapas do protocolo |
| POST | `/reproductions/{id}/executions` | Owner ou admin + propriedade | Registra execução de etapa |
| GET | `/reproductions/{id}/executions` | JWT + propriedade | Lista execuções da reprodução |
| POST | `/reproductions/{id}/birth` | Owner ou admin | Registra nascimento |

## Lacuna conhecida

O catálogo de protocolos e etapas é global e não recebe `property_id`; sua escrita
é exclusiva de admin. Eventos reprodutivos, execuções e nascimentos pertencem a
uma propriedade e exigem verificação de acesso.

## Regras de contrato

Rotas privadas exigem JWT, autorizacao e isolamento por propriedade. Testes devem cobrir token ausente, entrada invalida, recurso inexistente e tentativa entre tenants.
