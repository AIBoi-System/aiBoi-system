---
title: "Funcionalidades Incluídas no MVP"
type: reference
status: deprecated
owner: documentation
canonical: false
ai_index: false
last_verified: 2026-07-16
---
# Funcionalidades Incluídas no MVP

As funcionalidades foram agrupadas por domínio de negócio para facilitar a implementação e testes.

## 1. Conta e Autenticação
- **Registro de Usuário:** Criação de conta via e-mail com verificação de segurança (OTP).
- **Login Seguro:** Autenticação via JWT com suporte a persistência de sessão.
- **Recuperação de Senha:** Fluxo via código de segurança enviado ao e-mail.
- **Perfil:** Edição de dados básicos (nome, telefone, foto) e endereço.

## 2. Propriedade (Fazenda)
- **Gestão de Fazendas:** Cadastro de múltiplas propriedades rurais.
- **Seleção Ativa:** Funcionalidade para escolher em qual fazenda o usuário está trabalhando no momento (isolamento de dados).

## 3. Animais
- **Cadastro Individual:** Registro por brinco, nome, sexo, raça e data de nascimento.
- **Nascimento:** Registro simplificado de novos animais vinculando-os a uma matriz.
- **Óbito:** Baixa no inventário com registro de data e motivo da morte.

## 4. Lotes e Pastagens
- **Lotes:** Agrupamento de animais para manejo coletivo.
- **Piquetes:** Cadastro de subdivisões das pastagens com área em hectares.
- **Movimentação:** Registro de troca de lote de um piquete para outro.

## 5. Pesagem e Sanidade
- **Pesagem Manual:** Registro histórico do peso do animal.
- **Sanidade:** Cadastro de vacinas, vermífugos e tratamentos aplicados individualmente ou por lote.

## 6. Reprodução Básica
- **Histórico Reprodutivo:** Registro de coberturas e diagnósticos de prenhez simples.

## 7. Atividades e Alertas
- **Atividades:** Checklist de tarefas de campo pendentes e concluídas.
- **Alertas:** Notificações sobre animais que precisam ser vacinados ou lotes que excederam o tempo no piquete.

## 8. Dashboard e Relatórios
- **Dashboard:** Resumo visual (Pizza/Barras) do rebanho por categoria e status.
- **Histórico do Animal:** Linha do tempo completa de todos os eventos de um animal específico pesquisado pelo brinco.
- **Relatórios Básicos:** Lista de inventário atual e taxa de natalidade simples.

---

### Tabela de Resumo Operacional

| Funcionalidade | Objetivo | Usuário Principal | Prioridade |
| :--- | :--- | :--- | :--- |
| Cadastro Animal | Garantir inventário real. | Peão / Gerente | P0 (Crítica) |
| Offline Sync | Funcionar no pasto. | Todos | P0 (Crítica) |
| Dashboard | Visão rápida do rebanho. | Proprietário | P1 (Alta) |
| Movimentação | Controlar lotação. | Gerente | P1 (Alta) |
