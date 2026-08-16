---
title: "Escopo do MVP"
type: reference
status: deprecated
owner: documentation
canonical: false
ai_index: false
last_verified: 2026-07-16
---
# Escopo do MVP

O MVP do AiBoi é focado em digitalizar o inventário zootécnico e os manejos essenciais de campo para propriedades de cria, permitindo a substituição do caderno de campo por uma solução mobile offline-first.

## Definição do MVP
Uma aplicação Android para pequenos e médios pecuaristas que permite o controle individual de bovinos, gestão de lotes, pastagens e registros básicos de saúde, peso e reprodução.

## Objetivo
Validar se o produto reduz o tempo de registro de manejo e a perda de dados zootécnicos em ambientes de baixa conectividade.

## Problema que Resolve
- Perda de informações registradas em papel.
- Falta de histórico individual do animal no momento do manejo (curral).
- Dificuldade em calcular a lotação das pastagens (UA/ha).
- Esquecimento de datas críticas de vacinação e protocolos reprodutivos.

## Público
Pecuaristas e gerentes de propriedades de cria que buscam simplicidade e agilidade mobile.

## Módulos Incluídos
1.  **Acesso:** Autenticação e Perfil.
2.  **Infraestrutura:** Propriedades, Pastagens e Piquetes.
3.  **Inventário:** Animais, Lotes, Nascimentos e Óbitos.
4.  **Operacional:** Pesagens, Sanidade, Reprodução Básica e Atividades.
5.  **Inteligência:** Dashboard, Histórico Individual e Alertas.

## Principais Fluxos
- Registro de usuário e criação da primeira fazenda.
- Cadastro de animal e vínculo com matriz (mãe).
- Movimentação de lote entre piquetes.
- Registro de evento sanitário coletivo.

## Limitações do MVP
- **Plataforma:** Apenas Android.
- **Escopo de Atividade:** Exclusivo para Pecuária de Cria (não atende recria/engorda agora).
- **Entrada de Dados:** 100% manual (sem integração com hardware externo).
- **Relatórios:** Apenas consultas na tela e exportações básicas.

## Fronteira entre MVP e Visão Futura
A fronteira é demarcada pela **automação e financeiro**. O MVP lida com a **biologia e o manejo** do animal. Qualquer recurso que envolva transações monetárias (compra/venda), fiscais (GTA), ou dispositivos de hardware (sensores/IoT) está fora desta fase.
