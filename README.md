<div align="center">
  <h1>🐂 AiBoi - Sistema de Gestão para Pecuária 4.0</h1>
  <p><i>Transformando o manejo bovino através da digitalização e dados.</i></p>

  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</div>

---

## 📖 Sobre o Projeto

O **AiBoi** é uma solução de backend robusta desenvolvida para a digitalização do manejo bovino. O sistema foca em monitoramento zootécnico, controle reprodutivo, pesagem e gestão de pastagens, integrando tecnologias de ponta para otimizar a produção pecuária.

> **Status:** 🟢 Desenvolvimento Ativo (2026)

---

## 🚀 Tecnologias Utilizadas

| Tecnologia | Descrição |
| :--- | :--- |
| **Linguagem** | `Python 3.10` |
| **Framework** | `FastAPI` |
| **ORM** | `SQLAlchemy` |
| **Banco de Dados** | `MySQL` (AWS RDS em produção) |
| **Containerização** | `Docker` & `Docker Compose` |
| **Estilo de Código** | `PEP 8` |

---

## 🛠️ Pré-requisitos

Antes de começar, verifique se você possui:

- [x] **Git** instalado.
- [x] **Docker** e **Docker Compose** configurados.
- [x] **Python 3.10+** (opcional, para execução local sem Docker).

---

## 📥 Instalação e Configuração

### 1. Clonar o Repositório
```bash
git clone [https://github.com/seu-usuario/aiBoi-system.git](https://github.com/seu-usuario/aiBoi-system.git)
cd aiBoi-system
````
### 2. Variáveis de Ambiente 🔑

Crie um arquivo chamado `.env` na raiz do diretório `backend/`. Este arquivo é essencial para que a API consiga se comunicar com o banco de dados **MySQL/RDS**.

> [!IMPORTANT]
> **Atenção:** Nunca versione o arquivo `.env`. Certifique-se de que ele esteja listado no seu `.gitignore`.

Copie e cole o conteúdo abaixo no arquivo:

```env
# Formato: driver://usuario:senha@host:porta/nome_do_banco
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/aiboi_db
```

### 🗄️ Verificação e Documentação

O sistema possui rotas específicas para validar a saúde do projeto e facilitar os testes da equipe de forma rápida e visual:

| 🛠️ Recurso | 📝 Descrição | 🔗 Link de Acesso |
| :--- | :--- | :--- |
| **Status do Banco** | Valida a conexão em tempo real com o RDS/Local | [http://localhost:8000/test-db](http://localhost:8000/test-db) |
| **Swagger UI** | Documentação interativa para teste de endpoints | [http://localhost:8000/docs](http://localhost:8000/docs) |
| **ReDoc** | Documentação técnica em formato de página estática | [http://localhost:8000/redoc](http://localhost:8000/redoc) |

> [!TIP]
> **Produtividade:** Utilize o **Swagger UI** (`/docs`) para testar as rotas e os modelos de dados diretamente pelo navegador, dispensando o uso de ferramentas externas como Postman ou Insomnia durante o desenvolvimento.
