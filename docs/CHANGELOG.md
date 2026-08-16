---
title: "Changelog da documentacao"
type: governance
status: active
owner: documentation
canonical: true
ai_index: true
last_verified: 2026-08-14
---
# Changelog da documentacao

Todas as mudancas relevantes da documentacao sao registradas aqui.

## 2026-08-14

### Adicionado

- Compose local com API e Mailpit, imagem FastAPI não-root, healthcheck, contexto
  de build sem `.env` e conexão segura ao PostgreSQL instalado no host.
- Onboarding completo no README para PostgreSQL, API, Flutter, Mailpit e Google
  Antigravity 2.0.
- Configuração DBHub que interpola a senha do `.env` somente no processo e
  gerador local, sem segredo, do JSON do Antigravity.
- Runbook operacional do MCP PostgreSQL somente leitura para agentes.
- Home, menu lateral, propriedades, cadastro/sucesso de propriedade,
  configurações, perfil em quatro abas e catálogo de atividades implementados
  a partir dos frames Figma `3303:*` e `3224:*`.
- Rotas autenticadas `/properties`, `/activities`, `/settings` e `/profile`,
  com componentes compartilhados de cabeçalho, drawer e cartão.
- Testes de widget para configurações, abas do perfil e sete grupos de
  atividades.
- Regras canônicas de dependência DDD/SOLID para o backend e guardrails Pytest
  contra novas violações de camadas, contextos e raízes de agregado.
- Cadastro por etapas com OTP de e-mail e telefone, CPF one-to-one, endereço
  validado e senha liberada somente após as duas confirmações.
- Sessões persistidas e revogáveis, rotação de refresh token e logout real.
- Migration `7b9d2c4e6f81` para `cpfs`, `phone_verification_codes` e `auth_sessions`.
- Entrega local gratuita por Mailpit para e-mail e SMS simulado, limitada ao
  loopback e proibida em produção.
- Build Flutter Web local conectado à API e roteiro gráfico das seis etapas de
  cadastro com consulta dos OTPs no Mailpit.
- Telas de boas-vindas, escolha de autenticação, login por e-mail e sequência de
  cadastro implementadas a partir dos frames Figma `727:3463`, `727:3476`,
  `727:3504` e do guia visual `1254:2423`.

### Alterado

- Viewport Flutter Web limitado a 412 px e centralizado em telas largas,
  preservando o layout móvel sem alterar o comportamento em celulares menores.
- Home passou a representar o painel da propriedade ativa; a seleção de fazenda
  passou para a tela dedicada de propriedades.
- Consulta do dashboard de propriedade removida do router e orquestrada pela
  camada application, sem mudança no contrato HTTP.
- Router de autenticação reduzido à camada de apresentação; regras e persistência
  foram movidas para application/repository.
- Inicialização do Google Sign-In passou a ser opcional sem `GOOGLE_CLIENT_ID`,
  evitando tela branca no ambiente local de cadastro por e-mail.
- Visão de segurança atualizada: sem issues críticas ou altas, score local
  9,4/10 e bloqueio explícito de produção até validar SMS por operadora real.
- Design system de autenticação alinhado a botões e inputs de 60 px, raio de
  12 px, paleta verde oficial, fontes locais Poppins/Roboto e estados de hover,
  loading e desabilitado.

### Esclarecido

- Protocolos reprodutivos e etapas formam catalogo global consultavel por
  usuarios autenticados e gravavel somente por admin.
- `ENV=production` exige `REDIS_URL` alcancavel para rate limiting distribuido;
  fallback em memoria permanece restrito a desenvolvimento e testes.

## 2026-07-27

### Adicionado

- Guia canônico de início para desenvolvimento por humanos e agentes de IA.
- Estrutura completa da equipe, responsabilidades, RACI, handoffs e indicadores.
- Fluxo de entrega com contratos, gates, revisão e formato de evidências.
- Plano executável do MVP em ondas, com dependências e backlog pós-MVP.
- Agente `aiboi-postgres-dba` com checklist de migração e controles Supabase.
- Alembic, psycopg 3 e migration inicial PostgreSQL.
- ADR-007 para adoção do PostgreSQL gerenciado pelo Supabase.

### Alterado

- Removida a criação automática de tabelas no startup da API.
- Configuração de banco passou a normalizar URLs PostgreSQL do Supabase e expor
  parâmetros de pool.
- Identificação do animal passou a ser única por propriedade.
- MySQL/PyMySQL foi substituído por PostgreSQL/psycopg no backend.

### Esclarecido

- Offline, Bluetooth, pagamentos, financeiro, estoque e relatórios avançados
  permanecem pós-MVP apesar de constarem na especificação histórica.
- Decisões de escopo, termos centrais, fornecedores, arquitetura macro e questões
  legais permanecem sob autoridade humana.

## 2026-07-16

### Adicionado

- Estrutura documental numerada de 00 a 18.
- Indice geral, guia de contribuicao e especificacao mestra normalizada.
- Documentacao de produto, MVP, dominio, arquitetura, seguranca, dados, API, frontend e backend.
- Guias de qualidade, operacao, engenharia, modulos, roadmap, pesquisa e decisoes.
- Registro explicito de inconsistencias entre especificacao legada e codigo.
- Conteudo especifico para todas as paginas anteriormente classificadas como rascunho.
- ADRs completos, diagramas arquiteturais, exemplos de API/backend e runbooks operacionais.
- Especificacoes detalhadas de design system, estados e telas Flutter.

### Alterado

- 231 paginas genericas foram reclassificadas e preenchidas com objetivo, estado, regras, verificacao e referencias.
- O corpus de IA passou a indexar apenas paginas com conteudo especifico e metadados completos.

### Preservado

- Documentos anteriores em `docs/product`, `docs/mvp` e `docs/design-system.md` como fontes de migracao.
