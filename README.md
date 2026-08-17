# AgroFence

Plataforma de gestão pecuária com API FastAPI, aplicativo Flutter e PostgreSQL.
O repositório segue DDD, SOLID, separação por camadas e isolamento de dados por
propriedade.

## Estado atual

- Backend: FastAPI, SQLAlchemy 2, psycopg 3 e Alembic.
- Banco local: PostgreSQL 18 em `localhost:5432/db_agrofence`.
- Frontend: Flutter para Web, Android, iOS e desktop.
- Autenticação: cadastro por etapas, CPF separado, endereço validado, confirmação
  de e-mail e telefone, login, refresh token e logout.
- Testes locais de mensagens: Mailpit para e-mail e SMS simulado.
- MCP: DBHub em modo somente leitura para Codex e Google Antigravity 2.0.
- MySQL não faz parte da arquitetura ativa.

## Estrutura

```text
aiBoi-system/
├── backend/                 # API, ORM, migrations e testes
├── frontend/                # Aplicativo Flutter
├── config/mcp/              # Configuração MCP sem credenciais
├── docs/                    # Documentação canônica
├── scripts/                 # Configuração e inicialização local
└── docker-compose.yml
```

## Pré-requisitos no Windows

- Python 3.10 ou superior;
- PostgreSQL 18 e `psql`;
- Flutter compatível com o `pubspec.yaml`;
- Node.js 22.5 ou superior para o DBHub;
- Google Antigravity 2.0, se o acesso MCP for utilizado.

Valide as ferramentas:

```powershell
python --version
flutter --version
node --version
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" --version
```

## 1. Configurar o PostgreSQL local

Na raiz do repositório, execute:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup_agrofence_postgres.ps1
```

O configurador é idempotente: cria somente o que não existir e reaplica as
permissões necessárias. As senhas são solicitadas com entrada protegida e não
são impressas no terminal. Ele prepara:

| Item | Valor ou permissão |
| --- | --- |
| Banco | `db_agrofence` |
| Host e porta | `localhost:5432` |
| Aplicação | `agrofence_app`, com acesso de runtime e migrations |
| MCP | `codex_reader`, com `CONNECT`, `USAGE` e `SELECT` |
| Bloqueado ao leitor | `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `TRUNCATE` e sequences |

As credenciais são gravadas apenas em `.env` e `backend/.env`, ambos ignorados
pelo Git. Nunca copie senhas para README, código, commits ou configuração global
de agentes.

Depois, aplique as migrations:

```powershell
cd backend
.\.venv\Scripts\python.exe -m alembic -c alembic.ini upgrade head
.\.venv\Scripts\python.exe -m alembic -c alembic.ini current
cd ..
```

O Alembic é a única autoridade para criar ou alterar tabelas. A API não executa
`create_all` no startup.

## 2. Executar o ambiente local

### E-mail e telefone de teste

```powershell
powershell -ExecutionPolicy Bypass -File scripts\start_mailpit.ps1
```

Abra `http://127.0.0.1:8025`. Em desenvolvimento, os códigos de e-mail e o SMS
simulado aparecem no Mailpit. Isso valida o fluxo da interface, mas não comprova
a posse de um celular real; produção continua exigindo um provedor SMS.

### API

```powershell
cd backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Interface Flutter Web

Em outro terminal:

```powershell
cd frontend
flutter pub get
flutter run -d chrome --web-port 8080 --dart-define=API_BASE_URL=http://127.0.0.1:8000
```

| Serviço | URL |
| --- | --- |
| Interface | `http://127.0.0.1:8080` |
| API | `http://127.0.0.1:8000` |
| Swagger | `http://127.0.0.1:8000/docs` |
| Teste do banco | `http://127.0.0.1:8000/test-db` |
| Mailpit | `http://127.0.0.1:8025` |

### Alternativa: API e Mailpit com Docker

Com PostgreSQL já configurado no Windows e migrations aplicadas, inicie os
serviços de desenvolvimento em contêiner:

```powershell
docker compose up --build
```

O Compose lê `backend/.env`, conecta a API ao PostgreSQL local por
`host.docker.internal` e expõe apenas `127.0.0.1:8000`, `127.0.0.1:1025` e
`127.0.0.1:8025`. Ele não cria, apaga ou substitui o banco `db_agrofence`.

```powershell
docker compose ps
docker compose down
```

## 3. Configurar o MCP no Antigravity 2.0

O projeto usa `@bytebase/dbhub@0.24.0` por `stdio`. A versão é fixada para que a
configuração seja reproduzível. O arquivo versionado
[`config/mcp/dbhub-agrofence.toml`](config/mcp/dbhub-agrofence.toml) contém
somente host, porta, banco, usuário e limites seguros; a senha é interpolada em
memória a partir de `AGROFENCE_READER_PASSWORD` no `.env`.

Gere a configuração local do Antigravity:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\prepare_antigravity_mcp.ps1
```

O comando cria, sem senha, o arquivo ignorado pelo Git:

```text
.local-tools/antigravity-mcp-agrofence.json
```

Agora faça a única alteração global, manualmente:

1. No Antigravity, abra `...` → **MCP Servers** → **Manage MCP Servers** →
   **View raw config**.
2. O arquivo global no Windows é
   `%USERPROFILE%\.gemini\config\mcp_config.json`.
3. Copie o servidor `agrofence_postgres` do JSON gerado para a chave existente
   `mcpServers`. Preserve os outros servidores já configurados.
4. Salve e use **Refresh** em **Settings → Customizations**, ou reinicie o
   Antigravity.

Exemplo da estrutura, sem credenciais:

```json
{
  "mcpServers": {
    "agrofence_postgres": {
      "command": "C:\\Program Files\\nodejs\\npx.cmd",
      "args": [
        "-y",
        "@bytebase/dbhub@0.24.0",
        "--transport",
        "stdio",
        "--config",
        "C:\\caminho\\aiBoi-system\\config\\mcp\\dbhub-agrofence.toml"
      ],
      "cwd": "C:\\caminho\\aiBoi-system",
      "env": {
        "NODE_ENV": "production"
      },
      "disabled": false
    }
  }
}
```

`NODE_ENV=production` faz o DBHub carregar o `.env` a partir de `cwd` e
interpolar a variável usada pelo TOML. Essa variável de modo não é uma
credencial. Não coloque `env` com senha dentro do JSON global.

### Validar o MCP

No Antigravity CLI, execute `agy` e depois `/mcp`. No IDE, confirme que
`agrofence_postgres` aparece conectado. Faça apenas testes de leitura:

- “Liste os schemas do banco AgroFence.”
- “Liste as tabelas e colunas do schema public.”
- “Execute `SELECT version();`.”

O MCP possui duas barreiras independentes: `readonly = true` no DBHub e o papel
PostgreSQL `codex_reader` sem privilégios de escrita. Ele serve para inspeção e
consultas; migrations continuam sendo executadas pelo Alembic com
`agrofence_app`.

## Fluxo de cadastro e login

1. Escolha cadastro por e-mail ou Google.
2. Informe dados pessoais e confirme o e-mail por OTP.
3. Informe o telefone e confirme o segundo OTP.
4. Informe CPF e endereço válidos.
5. Crie a senha somente após as duas confirmações.
6. Cadastre uma propriedade ou siga para a Home.
7. Login cria uma sessão persistida; refresh rotaciona o token e logout revoga a
   sessão.

Alterações de cadastro, perfil, endereço, propriedade e dados pecuários exigem
usuário autenticado. O backend aplica autorização e isolamento por propriedade;
a interface não substitui essas verificações.

## Testes e qualidade

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m compileall -q app tests
cd ..\frontend
flutter analyze
flutter test
```

Padrões obrigatórios: PEP 8 e Ruff no backend, `dart format` e `flutter analyze`
no frontend, dependências DDD direcionadas para dentro e routers sem acesso
direto à persistência.

## Documentação

- [Backend](backend/README.md)
- [Frontend](frontend/README.md)
- [Banco de dados](docs/06-database/README.md)
- [Arquitetura](docs/04-architecture/README.md)
- [Operação do Antigravity e MCP](docs/11-operations/antigravity-mcp.md)
- [Segurança](docs/05-security/README.md)
