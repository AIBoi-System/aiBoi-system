<div align="center">

# AgroFence — Gestão para Pecuária 4.0

*Digitalização do manejo bovino com dados, reprodução, sanidade e propriedades.*

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Flutter](https://img.shields.io/badge/Flutter-3.11+-02569B?style=flat-square&logo=flutter&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)

**Status:** desenvolvimento ativo (2026)

</div>

---

## Sobre

O **AgroFence** é um monorepo para gestão pecuária: API REST em **FastAPI** (Clean Architecture + DDD) e aplicativo **Flutter** para produtores e equipe de campo.

| Módulo | Documentação |
| :--- | :--- |
| API, banco, Docker, testes | [backend/README.md](backend/README.md) |
| App mobile, fluxo de cadastro, UI | [frontend/README.md](frontend/README.md) |

---

## Estrutura do repositório

```text
AgroFence-system/
├── backend/          # API FastAPI + SQLAlchemy + MySQL
├── frontend/         # App Flutter (Android, iOS, Web, Desktop)
├── docker-compose.yml
├── global-bundle.pem # Certificado SSL AWS RDS (não versionar credenciais)
└── README.md         # Este arquivo
```

---

## Início rápido

### Com Docker (recomendado)

```bash
git clone https://github.com/seu-usuario/AgroFence-system.git
cd AgroFence-system
```

Crie `.env` na raiz (usado pelo `docker-compose`) — veja [backend/README.md](backend/README.md).

```bash
docker compose up --build
```

| Recurso | URL |
| :--- | :--- |
| API | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |
| Health DB | http://localhost:8000/test-db |

### App Flutter

```bash
cd frontend
flutter pub get
flutter run
```

Detalhes em [frontend/README.md](frontend/README.md).

---

## Fluxo de cadastro (app)

1. Boas-vindas → **Criar conta**
2. Acesso → **Continuar com e-mail**
3. Dados pessoais (nome, e-mail) → código enviado ao e-mail
4. Verificação do e-mail (código de 5 dígitos)
5. Criação de senha (requisitos de segurança)
6. Endereço do usuário (obrigatório para o cadastro no sistema)
7. Tela de conclusão → cadastro de propriedade (opcional)
8. Sucesso da propriedade → **Home** (minhas propriedades)

---

## Contribuição

1. `git pull origin main`
2. `git checkout -b feature/nome-da-tarefa`
3. Desenvolver com PEP 8 (backend) e `flutter analyze` (frontend)
4. Abrir Pull Request descrevendo a alteração e o requisito atendido

---

<div align="center">

*Iniciativa de modernização da pecuária no Pará.*

</div>
