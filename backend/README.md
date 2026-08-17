# AiBoi — Backend (API)

API REST em **FastAPI** com **SQLAlchemy**, **PostgreSQL/psycopg 3** e arquitetura em camadas (Clean Architecture + DDD).

---

## Stack

| Item | Tecnologia |
| :--- | :--- |
| Linguagem | Python 3.10+ |
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Banco | PostgreSQL 18 local; implantação gerenciada compatível |
| Driver | psycopg 3 |
| Migrations | Alembic |
| Auth | JWT (`python-jose`) + bcrypt |
| Testes | pytest + httpx |

---

## Estrutura

```text
backend/
├── app/
│   ├── application/       # Casos de uso e serviços
│   ├── domain/          # Entidades, enums e regras de domínio
│   ├── infrastructure/  # DB, auth, repositórios, modelos ORM
│   ├── presentation/    # Routers, schemas Pydantic, handlers
│   └── main.py          # Bootstrap FastAPI
├── tests/
├── Dockerfile
└── requirements.txt
```

---

## Pré-requisitos

- Python 3.10+ **ou** Docker + Docker Compose
- PostgreSQL acessível; o desenvolvimento local usa `localhost:5432/db_agrofence`

---

## Configuração

### Variáveis de ambiente

Crie `backend/.env` a partir de `.env.example`:

```env
DATABASE_URL=postgresql+psycopg://agrofence_app:YOUR_PASSWORD_URL_ENCODED@localhost:5432/db_agrofence
MIGRATION_DATABASE_URL=postgresql+psycopg://agrofence_app:YOUR_PASSWORD_URL_ENCODED@localhost:5432/db_agrofence
JWT_SECRET_KEY=your-long-random-secret
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
CORS_ALLOWED_ORIGINS=*
ENV=development
REDIS_URL=

# SMTP (required when ENV=production)
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=api@example.com
SMTP_PASSWORD=secret
SMTP_FROM_EMAIL=noreply@aiboi.com
SMTP_USE_TLS=true
```

See [`.env.example`](.env.example) for the full template.

> **Nunca** versione `.env` nem credenciais reais.

Em desenvolvimento e testes, `REDIS_URL` pode permanecer vazio e o rate limiter
usa memória local do processo. Em `ENV=production`, `REDIS_URL` é obrigatório e
deve responder no startup; fallback em memória não é aceito em produção porque
não coordena limites entre processos ou instâncias.

### Conexões locais e gerenciadas

No PostgreSQL local, use a conexão direta configurada em `DATABASE_URL`. Em um
provedor gerenciado, habilite TLS conforme o provedor e use conexão direta para
Alembic, backups e restaurações em `MIGRATION_DATABASE_URL`. Senhas com caracteres
reservados devem ser codificadas na URL.

---

## Executar

### Docker (raiz do monorepo)

```bash
docker compose up --build
```

O Compose usa o PostgreSQL local já configurado, sem criar outro banco: dentro
do contêiner, `DATABASE_HOST_OVERRIDE=host.docker.internal` troca apenas o host
da URL de runtime. Também inicia Mailpit em `http://127.0.0.1:8025`. Antes de
subir, aplique as migrations localmente com Alembic. Para parar o ambiente:

```bash
docker compose down
```

### Local

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m alembic -c alembic.ini upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Documentação e health

| Endpoint | Descrição |
| :--- | :--- |
| `GET /` | Status da API |
| `GET /test-db` | Teste de conexão PostgreSQL |
| `GET /docs` | Swagger UI |
| `GET /redoc` | ReDoc |

---

## Módulos da API (v1)

Rotas agregadas em `app/presentation/api/v1/router.py`:

| Prefixo | Domínio |
| :--- | :--- |
| `/auth` | Login, sessões, logout, reset e cadastro com verificação de e-mail e telefone |
| `/users` | Usuários |
| `/addresses` | Endereços |
| `/properties` | Propriedades rurais |
| `/animals`, `/health`, `/weighing` | Rebanho e sanidade |
| `/reproduction` | Reprodução |
| `/pastures`, `/paddocks` | Pastagens e piquetes |
| `/owners`, `/batches` | Proprietários e lotes |

### Cadastro de usuário

1. `POST /auth/signup/send-code` — envia o código ao e-mail.
2. `POST /auth/signup/verify-code` — confirma o e-mail.
3. `POST /auth/signup/send-phone-code` — envia o código ao telefone.
4. `POST /auth/signup/verify-phone-code` — confirma o telefone.
5. `POST /auth/signup/register` — valida CPF e endereço, cria o usuário e devolve a sessão.

Os códigos nunca são retornados pela API nem gravados em logs. No modo local,
e-mail e SMS simulado são capturados pelo Mailpit. O cadastro cria CPF e endereço
na mesma transação e só aceita a senha após as duas confirmações.

---

## Banco de dados

O startup da API não cria nem altera tabelas. Alembic é a autoridade do schema:

```bash
cd backend
python -m alembic -c alembic.ini upgrade head
python -m alembic -c alembic.ini current
```

Use `MIGRATION_DATABASE_URL` para separar a conexão administrativa da conexão
de runtime. Não aplique migrations em produção sem backup e validação em staging.

---

## Testes

```bash
cd backend
pytest
```

---

## Security (OWASP-oriented)

- **SQL injection:** SQLAlchemy ORM only (parameterized queries); no raw user input in SQL.
- **Input validation:** `app/core/security_validators.py` blocks dangerous patterns in text fields.
- **Email:** normalized and regex-validated before persistence (`EmailStr` + `normalize_email`).
- **Password policy:** minimum 8 chars, digit + symbol required on registration.
- **Rate limiting:** login e verificação de cadastro usam Redis compartilhado em
  produção; o fallback em memória é exclusivo de desenvolvimento e testes
  (`app/core/rate_limit.py`).
- **Headers:** CSP, `X-Frame-Options`, `X-Content-Type-Options` in `main.py`.

## Estilo de código

- PEP 8 — identifiers and module names in **English**
- Ferramentas sugeridas: **Black**, **Flake8** ou **Ruff**

```bash
docker compose logs -f   # logs em tempo real
```
