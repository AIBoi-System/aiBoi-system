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

<div align="center">
  <h1>🐂 AiBoi - Gestão Pecuária Inteligente</h1>
  <p><i>Digitalizando o manejo bovino com alta performance e precisão.</i></p>

  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</div>

---

## 📖 Visão Geral

O **AiBoi** é um ecossistema de backend focado na **Pecuária 4.0**. Desenvolvido para atender requisitos rigorosos de monitoramento zootécnico (REQ-030) e sanitário (REQ-031), o sistema permite o controle total de lotes, pesagens, reprodução e manejo de pastagens.

---

## 🛠️ Tecnologias e Padrões

* **Arquitetura:** Camadas (Controllers, Services, Repositories, Models).
* **Estilo:** `PEP 8` (Código limpo e padronizado).
* **Infraestrutura:** Dockerizada com suporte a AWS RDS.

---

## 📥 Instalação e Setup

### 1️⃣ Clonar Repositório
```bash
git clone [https://github.com/seu-usuario/aiBoi-system.git](https://github.com/seu-usuario/aiBoi-system.git)
cd aiBoi-system
