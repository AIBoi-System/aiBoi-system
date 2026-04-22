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
>
> ## 📂 Estrutura do Projeto

O **AiBoi** utiliza uma arquitetura em camadas para separar responsabilidades, facilitando a manutenção e a escalabilidade do sistema:

```plaintext
backend/app/
├── 🎮 controllers/   # Rotas e Endpoints da API (Entrada de dados)
├── 🧠 services/      # Lógica de negócio e cálculos zootécnicos (O "cérebro")
├── 🗄️ repositories/  # Camada de persistência e consultas (SQLAlchemy)
├── 📐 models/        # Entidades e Definição das Tabelas do Banco
├── 📝 schemas/       # Modelos Pydantic (Validação e Serialização JSON)
├── 🏷️ enums/         # Padronização de Tipos, Status e Categorias
├── ⚙️ core/          # Configurações globais, segurança e conexão DB
└── 🚀 main.py        # Ponto de entrada e inicialização do FastAPI
```

---

## 🛠️ Comandos de Manutenção

### 🔄 Sincronização do Banco de Dados
O sistema utiliza o mapeamento do **SQLAlchemy** para gerenciar o esquema do banco de dados. A criação das tabelas no **AWS RDS** ou ambiente local ocorre automaticamente na inicialização da aplicação.

> [!IMPORTANT]
> **Ponto de Atenção:** Para que uma tabela seja criada, o modelo correspondente **DEVE** estar explicitamente importado no arquivo `main.py`. Caso contrário, o motor do SQLAlchemy não reconhecerá a classe e a tabela não será gerada.

### 🧹 Resetar Ambiente Docker
Se houver necessidade de limpar o ambiente, remover containers órfãos ou resetar completamente o banco de dados de desenvolvimento local, utilize o comando abaixo:

```bash
# Para parar os serviços e REMOVER os volumes de dados (Limpeza total)
docker-compose down -v
```
> [!CAUTION]
Aviso de Segurança: O parâmetro -v apaga permanentemente todos os volumes de dados vinculados. Use este comando apenas se tiver certeza de que não há dados de teste críticos no banco local que precisem ser preservados.
>
> ## 💡 Dicas de Desenvolvimento

Para garantir que o fluxo de trabalho da equipe seja fluido e o hardware se mantenha saudável, siga estas recomendações:

### 📡 Logs em Tempo Real
Para depurar erros de lógica ou visualizar as queries SQL sendo executadas pelo SQLAlchemy em tempo real, utilize o comando:

```bash
# Acompanha a saída de todos os containers em tempo real
docker-compose logs -f
```

### 📏 Padronização PEP 8

Para manter a integridade e a estética do código no projeto **AiBoi**, é obrigatório o uso de um linter (como **Flake8** ou **Black**). 

* **Consistência:** Garante que as camadas de `models/`, `schemas/` e `repositories/` sigam a mesma estrutura visual.
* **Agilidade:** Facilita o processo de *Code Review*, permitindo que a equipe foque na lógica e não na formatação.

---

### 🌡️ Monitoramento Térmico

> [!TIP]
> **Atenção ao Hardware:** Como o sistema utiliza modelos **YOLO** (*You Only Look Once*) para processamento de visão computacional, o uso da GPU (como a **RTX 3050**) pode ser extremamente intensivo.
>
> Monitore a temperatura do hardware durante treinamentos ou inferências prolongadas para evitar o *thermal throttling* (queda de desempenho por calor) ou danos físicos aos componentes.
