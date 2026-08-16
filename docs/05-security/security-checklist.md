---
title: "Checklist de seguranca"
type: reference
status: active
owner: security
canonical: true
ai_index: true
last_verified: 2026-08-14
---
# Checklist de seguranca

- [ ] Segredos fora do Git e rotacionados.
- [ ] Aplicacao falha ao iniciar sem chave JWT forte.
- [ ] Recuperacao envia token por canal seguro e responde genericamente.
- [ ] Todas as rotas privadas exigem JWT valido.
- [ ] Consulta usa ID e propriedade autorizada.
- [ ] Criacao ignora tenant arbitrario enviado pelo cliente.
- [ ] Atualizacao bloqueia campos protegidos.
- [ ] Logs nao possuem senha, token, CPF ou chave.
- [ ] CORS possui origens explicitas por ambiente.
- [ ] Erros nao retornam SQL, stack trace ou configuracao.
- [ ] Dependencias passam por verificacao de vulnerabilidade.
- [ ] Testes cobrem BOLA, autenticacao, rate limit e enumeracao.
- [ ] `ENV=production` exige `REDIS_URL` e falha no startup quando Redis nao esta alcancavel.
- [ ] Somente admin grava o catalogo global de protocolos e etapas.
