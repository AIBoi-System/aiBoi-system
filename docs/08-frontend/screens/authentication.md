---
title: "Tela: Authentication"
type: reference
status: partial
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Tela: Authentication

## Objetivo e estado

Boas-vindas, login, logout e cadastro guiado. A entrada oferece escolha explícita
entre e-mail e Google; e-mail abre o formulário de e-mail/senha no login e inicia
o fluxo guiado no cadastro. O cadastro segue e-mail, confirmação de e-mail,
telefone, confirmação de telefone, CPF/endereço e senha. A senha não é solicitada
antes das duas confirmações. Login mantém access e refresh tokens apenas em
memória nesta etapa; logout chama a API e sempre limpa a sessão local.

## Referência visual implementada

- Base móvel de 412 x 917, responsiva para telas menores e maiores.
- Ações principais e campos possuem 60 px de altura e raio de 12 px.
- O cabeçalho exibe nome da etapa, contador de 1/6 a 6/6 e segmentos de progresso.
- O login Google no Web exige `GOOGLE_CLIENT_ID`; sem a configuração, a interface
  apresenta erro recuperável e mantém o login por e-mail disponível.
- A tela de boas-vindas usa o asset exportado do Figma e não depende de URL
  temporária.

## Estados obrigatórios

Loading, conteúdo, vazio quando aplicável, validação, erro recuperável, permissão negada e sucesso confirmado pela API.

## Segurança e dados

A tela não concede autorização. Recursos operacionais usam a propriedade ativa e o backend valida ownership. Não exibir token, senha, CPF completo ou erro interno.

## Responsividade e testes

Conteúdo deve funcionar em 320 px, com teclado aberto e texto ampliado. Testar
navegação, ação principal, erro da API e ausência de dados. A implementação foi
comparada visualmente em 412 x 917 e não apresentou erro no console.
