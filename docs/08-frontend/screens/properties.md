---
title: "Tela: Propriedades"
type: reference
status: active
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Tela: Propriedades

## Objetivo e estado

Lista as propriedades acessíveis ao usuário autenticado, com filtros de ativas,
inativas e busca, além da ação de cadastro. Cada cartão apresenta nome,
localização, finalidade e área e permite selecionar a fazenda no Home.

O cadastro usa os estados de loading e erro do `RegistrationCubit`, envia os
dados à API e só mostra a tela de sucesso após confirmação do backend.

## Segurança e dados

A lista exige token e o backend aplica ownership. O estado de erro recuperável
é exibido quando a API rejeita ou não responde; a interface não cria dados
locais como se fossem persistidos.

## Responsividade e testes

O fluxo segue os frames Figma `3303:813`, `3303:942` e `3303:1020`, com largura
de referência de 400 px e viewport Web limitado a 412 px.
