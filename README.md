# Dashboard Bolsa x Macroeconomia

## Objetivo
Construir um dashboard em Power BI que analisa o desempenho histórico de ações da B3 e sua relação com indicadores macroeconômicos (Selic, IPCA), usando um pipeline em Python para extração e tratamento dos dados — com o objetivo de identificar padrões entre cenário macro e comportamento de ações.

## Fontes de Dados
- **Cotações de ações (B3):** Yahoo Finance, via biblioteca yfinance. Período: 2021-08-30 a 2026-08-26 (5 anos, dados diários).
  - Ativos: PETR4, VALE3, ITUB4, WEGE3, MGLU3, ABEV3, CPFE3, e o índice Ibovespa (^BVSP)
- **Selic:** Banco Central do Brasil, API SGS (série 432 - Meta Selic), dados diários.
- **IPCA:** Banco Central do Brasil, API SGS (série 433 - variação mensal), dados mensais.

## Modelo de Dados
Modelo em estrela no Power BI:
- **fato_retornos**: retornos mensais, preços, Selic e IPCA por ativo/mês
- **dim_ativos**: ticker, empresa, setor
- **dim_datas**: ano_mes, ano, mês

Principais medidas DAX: Retorno Acumulado %, Retorno Médio Mensal %, Volatilidade (Desvio Padrão), Selic Média, IPCA Médio Mensal, Preço Base 100 (normalizado para comparação entre ativos).

## Páginas do Dashboard
- **Visão Geral**: KPIs de contexto macro (Selic e IPCA médios do período), ranking de retorno acumulado por ativo, evolução dos preços normalizados (base 100) para comparação entre ativos de escalas diferentes.
- **Comparativo entre Ações**: segmentação por ativo, gráfico de dispersão risco x retorno (volatilidade vs. retorno médio mensal), tabela detalhada com todas as métricas por ativo e setor.

## Status do projeto
🚧 Em desenvolvimento — 2 de 3 páginas do dashboard concluídas (Visão Geral e Comparativo entre Ações). Próxima etapa: página Ações x Macro (Selic e IPCA).

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
