---
title: "Cenarios de teste do MVP"
type: reference
status: active
owner: product
canonical: true
ai_index: true
last_verified: 2026-07-16
---
# Cenarios de teste do MVP

| CT | Cenario | Resultado |
|---|---|---|
| CT001 | Login valido e invalido | Token apenas para credencial valida |
| CT002 | Token expirado | 401 sem detalhes internos |
| CT003 | Usuario A consulta propriedade de B | 404 |
| CT004 | Usuario A consulta animal de B alterando IDs | 404 |
| CT005 | Criar animal com identificacao repetida na mesma propriedade | Conflito |
| CT006 | Repetir identificacao em propriedades diferentes | Permitido |
| CT007 | Criar lote sem propriedade valida | Rejeitado |
| CT008 | Vincular sanidade a animal de outra propriedade | Rejeitado |
| CT009 | Solicitar recuperacao de senha | Resposta generica, token somente por canal seguro |
| CT010 | Fluxo Flutter com API indisponivel | Estado de erro recuperavel |
| CT011 | Tela em 320 px de largura | Sem sobreposicao ou corte |
| CT012 | Executar suite completa | Todos os testes verdes |
