# Requisitos do MVP

Os requisitos abaixo foram re-numerados para o contexto exclusivo do MVP do AiBoi.

## 1. Requisitos Funcionais (RF)

| Código | Título | Descrição | Prioridade |
| :--- | :--- | :--- | :--- |
| **MVP-RF001** | Autenticar usuário | Permitir criação de conta, login e reset de senha via e-mail. | Alta |
| **MVP-RF002** | Gerenciar perfil | Permitir edição de dados pessoais e endereço do proprietário. | Média |
| **MVP-RF003** | Gerenciar propriedade | CRUD de fazendas vinculadas ao usuário logado. | Alta |
| **MVP-RF004** | Selecionar propriedade | Alterar o contexto de trabalho para uma fazenda específica. | Alta |
| **MVP-RF005** | Gerenciar animal | CRUD individual de bois com identificação por brinco única. | Crítica |
| **MVP-RF006** | Registrar nascimento | Cadastrar novo animal vinculando-o à sua matriz (mãe). | Alta |
| **MVP-RF007** | Registrar morte | Dar baixa em um animal registrando data e causa. | Alta |
| **MVP-RF008** | Gerenciar lote | Criar agrupamentos lógicos de animais para manejos. | Média |
| **MVP-RF009** | Gerenciar pastagem | Cadastro de áreas globais de pastejo. | Baixa |
| **MVP-RF010** | Gerenciar piquete | Cadastro de subdivisões de pasto com tamanho em hectares. | Média |
| **MVP-RF011** | Movimentar animais | Registrar troca de lote ou animal entre piquetes diferentes. | Média |
| **MVP-RF012** | Registrar pesagem | Histórico manual de peso (kg) e data da leitura. | Alta |
| **MVP-RF013** | Sanidade básica | Registro de aplicações de vacinas e medicamentos. | Alta |
| **MVP-RF014** | Reprodução básica | Registro de cobertura e diagnóstico simples de prenhez. | Baixa |
| **MVP-RF015** | Gerenciar atividades | Visualização e baixa em lista de tarefas de manejo. | Média |
| **MVP-RF016** | Exibir alertas | Avisos sobre vacinas vencidas ou lotação excedida. | Média |
| **MVP-RF017** | Exibir dashboard | Visão geral quantitativa do rebanho na tela inicial. | Alta |
| **MVP-RF018** | Gerar histórico | Linha do tempo completa das ações realizadas no animal. | Alta |
| **MVP-RF019** | Relatórios básicos | Listagens filtradas para conferência de inventário. | Média |

## 2. Requisitos Não Funcionais (RNF)

| Código | Título | Descrição |
| :--- | :--- | :--- |
| **MVP-RNF001** | Plataforma Android | O sistema deve rodar nativamente em Android 9.0 ou superior. |
| **MVP-RNF002** | Funcionamento Offline | O app deve permitir registros sem internet e sincronizar depois. |
| **MVP-RNF003** | Desempenho Local | Consultas simples devem responder em menos de 1 segundo localmente. |
| **MVP-RNF004** | Segurança de Dados | Dados de uma fazenda não podem ser vistos por donos de outras. |
| **MVP-RNF005** | Persistência | Os dados locais não devem ser perdidos ao fechar o aplicativo. |

## 3. Requisitos de Usabilidade
- **Baixa Carga Cognitiva:** Máximo de 3 cliques para as tarefas mais frequentes (Pesagem/Nascimento).
- **Interface Curral-Friendly:** Uso de botões grandes e alto contraste para uso sob luz solar.

## 4. Requisitos de Segurança
- Criptografia de senhas (Bcrypt).
- Autenticação via tokens JWT com tempo de expiração.
- Validação de formato de CPF e E-mail em todas as entradas.
