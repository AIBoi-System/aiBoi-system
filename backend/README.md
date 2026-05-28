# AiBoi — Backend (API)

API REST em **FastAPI** com **SQLAlchemy**, **MySQL** e arquitetura em camadas (Clean Architecture + DDD).

---

## Stack

| Item | Tecnologia |
| :--- | :--- |
| Linguagem | Python 3.10+ |
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Banco | MySQL (local ou AWS RDS) |
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
- MySQL acessível (container ou RDS)

---

## Configuração

### Variáveis de ambiente

Crie `backend/.env` (ou `.env` na raiz do monorepo para o Docker):

```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/aiboi_db
JWT_SECRET_KEY=sua-chave-secreta-longa
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
CORS_ALLOWED_ORIGINS=*
```

> **Nunca** versione `.env` nem credenciais reais.

### SSL com AWS RDS

Na raiz do monorepo existe `global-bundle.pem`. Configure o caminho no módulo de conexão do banco quando usar RDS com SSL.

---

## Executar

### Docker (raiz do monorepo)

```bash
docker compose up --build
```

### Local

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Documentação e health

| Endpoint | Descrição |
| :--- | :--- |
| `GET /` | Status da API |
| `GET /test-db` | Teste de conexão MySQL |
| `GET /docs` | Swagger UI |
| `GET /redoc` | ReDoc |

---

## Módulos da API (v1)

Rotas agregadas em `app/presentation/api/v1/router.py`:

| Prefixo | Domínio |
| :--- | :--- |
| `/auth` | Login, JWT, reset de senha, **cadastro com verificação de e-mail** |
| `/users` | Usuários |
| `/addresses` | Endereços |
| `/properties` | Propriedades rurais |
| `/animals`, `/health`, `/weighing` | Rebanho e sanidade |
| `/reproduction` | Reprodução |
| `/pastures`, `/paddocks` | Pastagens e piquetes |
| `/owners`, `/batches` | Proprietários e lotes |

### Cadastro de usuário

1. `POST /auth/signup/send-code` — envia código de 5 dígitos ao e-mail (em dev o código pode vir na resposta).
2. `POST /auth/signup/verify-code` — valida o código antes de definir a senha.
3. `POST /auth/signup/register` — cria **endereço** + **usuário** (e-mail deve estar verificado).

O usuário exige `address_id` no modelo; o cadastro unificado cria o endereço na mesma requisição.

---

## Banco de dados

Na subida, `Base.metadata.create_all` cria/atualiza tabelas. Modelos precisam estar importados em `app/infrastructure/persistence/models/__init__.py`.

```bash
# Reset total do ambiente Docker (apaga volumes)
docker compose down -v
```

---

## Testes

```bash
cd backend
pytest
```

---

## Estilo de código

- PEP 8
- Ferramentas sugeridas: **Black**, **Flake8** ou **Ruff**

```bash
docker compose logs -f   # logs em tempo real
```
