---
title: "Boas praticas de documentacao para IA"
type: explanation
status: active
owner: documentation
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Boas praticas de documentacao para IA

## Principios adotados

1. Separar tutorial, guia pratico, referencia e explicacao segundo Diataxis.
2. Usar Markdown com hierarquia logica e secoes semanticamente coerentes.
3. Manter documentos pequenos o suficiente para recuperacao, sem fragmentar um tema artificialmente.
4. Adicionar metadados de tipo, estado, proprietario, fonte e data.
5. Indexar apenas conteudo canonico e excluir fontes brutas, legadas ou sensiveis.
6. Oferecer um indice compacto para agentes por meio de llms.txt.
7. Validar automaticamente links, metadados, duplicacao e higiene do corpus.

## Referencias pesquisadas

- [Diataxis](https://diataxis.fr/): quatro necessidades documentais e organizacao orientada ao usuario.
- [Google Developer Documentation Style Guide](https://developers.google.com/style): clareza, consistencia, acessibilidade, titulos e links descritivos.
- [Azure AI Search: chunking](https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents): fragmentacao por estrutura e coerencia semantica.
- [Azure Architecture Center: enriquecimento de chunks](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-enrichment-phase): limpeza e metadados para melhorar recuperacao.
- [llms.txt](https://llmstxt.org/): proposta experimental de indice Markdown para modelos de linguagem.

## Limites

llms.txt nao e um padrao universal nem substitui sitemap, OpenAPI, autorizacao ou um pipeline de RAG avaliado. Metadados melhoram filtragem, mas nao corrigem conteudo impreciso. Toda pagina gerada por IA precisa de revisao do proprietario antes de se tornar canonica.
