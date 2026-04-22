# 🐂 AiBoi - Sistema de Gestão para Pecuária 4.0

O **AiBoi** é uma solução de backend robusta desenvolvida para a digitalização do manejo bovino. O sistema foca em monitoramento zootécnico, controle reprodutivo, pesagem e gestão de pastagens, integrando tecnologias de ponta para otimizar a produção pecuária.

---

## 🚀 Tecnologias Utilizadas

* **Linguagem:** `Python 3.10`
* **Framework:** `FastAPI`
* **ORM:** `SQLAlchemy` (Mapeamento Objeto-Relacional)
* **Banco de Dados:** `MySQL` (AWS RDS em produção)
* **Containerização:** `Docker` & `Docker Compose`
* **Estilo de Código:** `PEP 8`

---

## 🛠️ Pré-requisitos

Antes de começar, você precisará ter instalado em sua máquina:

* [ ] **Git**
* [ ] **Docker** e **Docker Compose**
* [ ] **Python 3.10** ou superior (para execução local fora do Docker)

---

## 📥 Instalação e Configuração

### 1. Clonar o Repositório
bash
git clone [https://github.com/seu-usuario/aiBoi-system.git](https://github.com/seu-usuario/aiBoi-system.git)
cd aiBoi-system

2. Variáveis de Ambiente
Crie um arquivo chamado .env na raiz do diretório backend/ e configure as credenciais do banco de dados (use o arquivo .env.example como base):

Snippet de código
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/aiboi_db
3. Execução com Docker (Recomendado)
A maneira mais fácil de rodar o projeto é via Docker, que já configura o banco de dados e a API automaticamente:

Bash
docker-compose up --build
A API estará disponível em: http://localhost:8000

💻 Execução Local (Desenvolvimento)
Se preferir rodar sem Docker para depuração rápida:

1. Criar Ambiente Virtual
PowerShell
# No Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
2. Instalar Dependências
Bash
pip install -r requirements.txt
3. Iniciar a Aplicação
Bash
uvicorn main:app --reload
🗄️ Verificação do Banco de Dados
Para garantir que a conexão com o banco de dados (MySQL/RDS) está funcionando corretamente, você pode acessar o endpoint de teste:

🔗 Status do Banco: http://localhost:8000/test-db

📂 Estrutura do Projeto
O projeto segue uma arquitetura em camadas para facilitar a manutenção:

Plaintext
backend/app/
├── controllers/   # Rotas da API (Endpoints)
├── services/      # Lógica de negócio e regras zootécnicas
├── repositories/  # Comunicação direta com o banco de dados
├── models/        # Entidades SQLAlchemy (Tabelas)
├── schemas/       # Modelos Pydantic (Validação de dados)
├── enums/         # Definições de tipos fixos (Status, Sexo, etc)
├── core/          # Configurações globais e banco de dados
└── main.py        # Ponto de entrada da aplicação
📖 Documentação da API
Uma vez que o servidor esteja rodando, você pode acessar a documentação interativa (Swagger UI) para visualizar e testar todos os endpoints:

🔗 Swagger: http://localhost:8000/docs

🛠️ Comandos Úteis
Recriar Tabelas: O sistema está configurado para criar as tabelas automaticamente no banco de dados assim que o main.py é iniciado.

Limpar Docker: Remove containers e volumes (limpa o banco):

Bash
docker-compose down -v
👥 Contribuição
Faça um Pull da main antes de iniciar qualquer tarefa.

Crie uma branch para sua feature:

Bash
git checkout -b feature/nome-da-feature
Mantenha o padrão PEP 8 em todos os arquivos.

Submeta o Pull Request para revisão.

Nota: Este projeto é parte da iniciativa de modernização da pecuária no Pará. Em caso de dúvidas, consulte o líder técnico da equipe.
