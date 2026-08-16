---
title: "Antigravity 2.0 e MCP PostgreSQL"
type: runbook
status: active
owner: operations
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Antigravity 2.0 e MCP PostgreSQL

## Objetivo

Permitir que o Google Antigravity 2.0 inspecione o PostgreSQL local do
AgroFence sem receber privilégios de escrita nem armazenar senha em sua
configuração global.

## Contrato vigente

| Item | Configuração |
| --- | --- |
| Implementação MCP | `@bytebase/dbhub@0.24.0` |
| Transporte | `stdio` |
| Banco | `localhost:5432/db_agrofence` |
| Papel | `codex_reader` |
| Configuração DBHub | `config/mcp/dbhub-agrofence.toml` |
| Configuração Antigravity | `%USERPROFILE%\.gemini\config\mcp_config.json` |

## Preparação

1. Execute `scripts/setup_agrofence_postgres.ps1` e informe as senhas no prompt
   protegido.
2. Confirme Node.js 22.5 ou superior com `node --version`.
3. Execute `scripts/prepare_antigravity_mcp.ps1`.
4. Revise `.local-tools/antigravity-mcp-agrofence.json`.
5. No Antigravity, abra **MCP Servers → Manage MCP Servers → View raw config**.
6. Mescle `agrofence_postgres` dentro de `mcpServers`, preservando entradas já
   existentes, e atualize os servidores.

O preparador não altera arquivos fora do repositório. A mudança global é manual
e deve ser confirmada pelo responsável pelo computador.

## Tratamento de segredo

O TOML versionado usa `${AGROFENCE_READER_PASSWORD}`. A entrada MCP define
somente `NODE_ENV=production`, para o DBHub carregar o `.env` a partir do
diretório de trabalho e interpolar a senha em memória. `.env`, `backend/.env` e
`.local-tools/` são ignorados pelo Git.

É proibido copiar a senha para:

- `mcp_config.json`;
- README ou documentação;
- configuração versionada;
- código, logs, issues ou commits.

## Controles de leitura

O DBHub limita `execute_sql` a leitura e a 500 linhas. Esse controle não é a
fronteira principal: o PostgreSQL também nega escrita ao papel `codex_reader`,
mantém a sessão read-only e não concede sequences. Assim, uma falha do cliente
MCP não transforma o leitor em papel de aplicação.

## Verificação

No Antigravity CLI, inicie `agy` e use `/mcp`. No IDE, confirme o estado ativo do
servidor e solicite somente:

```sql
SELECT version();
SELECT schema_name FROM information_schema.schemata ORDER BY schema_name;
```

Também é seguro usar `search_objects` para listar schemas, tabelas e colunas.
Não use o MCP para migrations, seeds ou manutenção.

## Falhas comuns

- **Senha ausente:** execute novamente o configurador PostgreSQL; não a passe em
  argumento de linha de comando.
- **`node` não encontrado:** instale Node.js 22.5+ e reabra o terminal.
- **Servidor inativo:** confira os caminhos absolutos de `npx.cmd` e do TOML no
  JSON gerado e use Refresh no Antigravity.
- **Conexão recusada:** valide o serviço PostgreSQL, `localhost:5432` e a conexão
  de `codex_reader` pelo configurador.
- **Permissão negada para escrita:** comportamento esperado; o MCP é somente
  leitura.
