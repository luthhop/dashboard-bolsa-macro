# Dashboard Bolsa x Macroeconomia

## Objetivo
Construir um dashboard em Power BI que analisa o desempenho histórico de ações da B3 e sua relação com indicadores macroeconômicos (Selic, IPCA), usando um pipeline em Python para extração e tratamento dos dados — com o objetivo de identificar padrões entre cenário macro e comportamento de ações.

## Fontes de Dados
- **Cotações de ações (B3):** Yahoo Finance, via biblioteca yfinance. Período: 2021-08-30 a 2026-08-26 (5 anos, dados diários).
  - Ativos: PETR4, VALE3, ITUB4, WEGE3, MGLU3, ABEV3, CPFE3, e o índice Ibovespa (^BVSP)
- **Selic:** Banco Central do Brasil, API SGS (série 432 - Meta Selic), dados diários.
- **IPCA:** Banco Central do Brasil, API SGS (série 433 - variação mensal), dados mensais.

## Status do projeto
🚧 Em desenvolvimento — ingestão de dados concluída, próxima etapa: tratamento e modelagem dos dados

## Estrutura do repositório
- `data/raw` — dados brutos, como extraídos da fonte
- `data/processed` — dados tratados, prontos para o Power BI
- `src` — scripts Python de extração e tratamento
- `dashboard` — arquivo .pbix do Power BI
- `docs` — documentação e prints do dashboard

## Tecnologias
- Python (Pandas, yfinance)
- Power BI
- Git/GitHub

## Autor
Lucas — estudante de Ciência da Computação (UNINTER), em transição de Operações para Dados/Analytics.
