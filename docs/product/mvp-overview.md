---
title: "Visão Geral do MVP (Minimum Viable Product)"
type: explanation
status: deprecated
owner: documentation
canonical: false
ai_index: false
last_verified: 2026-07-16
---
# Visão Geral do MVP (Minimum Viable Product)

O MVP do AiBoi foca na base sólida de gerenciamento zootécnico para propriedades de cria, garantindo que o ciclo "Animal -> Manejo -> Histórico" funcione sem fricção.

## Definição do MVP
Uma ferramenta mobile para Android que permite o inventário completo de bovinos, controle de pesagens, sanidade básica e movimentação entre áreas da fazenda, com suporte a múltiplas propriedades sob uma mesma conta de Proprietário.

## Módulos Incluídos
- **Auth & Acesso:** Registro de usuário, verificação de e-mail e login seguro.
- **Gestão de Espaço:** Cadastro de Propriedades e Piquetes/Pastagens.
- **Inventário Animal:** Cadastro individual (Brinco, Sexo, Raça), Nascimentos e Óbitos.
- **Manejo de Lotes:** Criação de grupos e transferência entre piquetes.
- **Saúde & Pesagem:** Registro de vacinas/medicamentos e acompanhamento de peso manual.
- **Dashboards:** Resumo do rebanho por categoria e alertas imediatos.

## Principais Fluxos
1. **Registro e Setup:** Usuário se cadastra -> Cria primeira propriedade -> Cria primeiro piquete.
2. **Ciclo do Animal:** Registra nascimento de bezerro -> Vincula à matriz (mãe) -> Adiciona ao lote.
3. **Manejo de Campo:** Seleciona lote -> Move para novo piquete -> Registra pesagem coletiva.
4. **Consulta:** Busca por brinco -> Visualiza histórico completo do boi -> Registra óbito se necessário.

## Funcionalidades Excluídas (Fora do MVP)
- Emissão de GTA (Guia de Trânsito Animal).
- Integração via Bluetooth com balanças.
- Gestão de funcionários e permissões detalhadas.
- Controle financeiro de lucros e perdas.
- Gestão de estoque de ração e ferramentas.
- Inteligência Artificial para reconhecimento facial.

## Critérios de Conclusão
- Sincronização offline/online funcionando perfeitamente.
- Todos os campos obrigatórios zootécnicos validados no backend.
- Relatórios de inventário gerados corretamente em formato simples.

## Limitações Conhecidas
- O sistema depende exclusivamente da inserção manual de dados pelo usuário.
- Requer sistema Android (versão mínima a ser definida).
- A primeira versão pode apresentar lentidão em sincronizações com mais de 5.000 animais simultâneos.
