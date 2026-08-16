---
title: "Docker Compose"
type: reference
status: active
owner: operations
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Docker Compose

## Objetivo

Serviços, rede, variáveis e ciclo de vida do ambiente composto.

## Serviços

| Serviço | Porta local | Responsabilidade |
| --- | --- | --- |
| `api` | `127.0.0.1:8000` | API FastAPI ligada ao PostgreSQL local |
| `mailpit` | `127.0.0.1:1025`, `127.0.0.1:8025` | SMTP e interface de confirmação local |

O Compose não cria PostgreSQL. A API usa `backend/.env` e aplica
`DATABASE_HOST_OVERRIDE=host.docker.internal` apenas no runtime do contêiner.
Assim, a mesma credencial local não é duplicada em YAML nem em imagem.

## Uso

```powershell
docker compose up --build
docker compose ps
docker compose logs -f api
docker compose down
```

Execute `alembic upgrade head` antes de subir a API. O healthcheck da API consulta
somente a rota raiz; ele não cria nem altera dados.

## Regras

- Produção não usa segredo versionado.
- Mudança possui rollback e verificação.
- Operação é repetível e observável.
- Backup só é válido após teste de restauração.

## Critérios de verificação

- Comportamento principal e falhas possuem passos reproduzíveis.
- Entradas, saídas, dependências e responsáveis estão explícitos.
- Segurança, tenant e dados sensíveis foram avaliados.
- Testes e documentação são atualizados na mesma alteração.

## Referências

- [Environment Setup](environment-setup.md)
- [Secrets Management](../05-security/secrets-management.md)
- [Api Unavailable](runbooks/api-unavailable.md)
