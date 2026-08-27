import os

import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")


def tratar_cotacoes():
    df = pd.read_csv(os.path.join(RAW_DIR, "cotacoes_acoes.csv"), parse_dates=["Date"])

    # "Close" já vem ajustado — yfinance com auto_adjust=True (padrão) incorpora
    # splits e dividendos no Close e remove a coluna "Adj Close".

    df["ano_mes"] = df["Date"].dt.to_period("M")

    mensal = (
        df.sort_values("Date")
        .groupby(["Ticker", "ano_mes"])
        .last()
        .reset_index()[["ano_mes", "Ticker", "Close"]]
    )
    mensal = mensal.rename(columns={"Close": "preco_fechamento", "Ticker": "ticker"})

    mensal = mensal.sort_values(["ticker", "ano_mes"])
    mensal["retorno_mensal_pct"] = (
        mensal.groupby("ticker")["preco_fechamento"]
        .pct_change()
        .mul(100)
    )

    return mensal


def tratar_selic():
    df = pd.read_csv(os.path.join(RAW_DIR, "selic.csv"), parse_dates=["data"])
    df["ano_mes"] = df["data"].dt.to_period("M")
    mensal = df.groupby("ano_mes")["valor"].mean().reset_index()
    mensal = mensal.rename(columns={"valor": "selic_media"})
    return mensal


def tratar_ipca():
    df = pd.read_csv(os.path.join(RAW_DIR, "ipca.csv"), parse_dates=["data"])
    df["ano_mes"] = df["data"].dt.to_period("M")
    df = df.rename(columns={"valor": "ipca_variacao"})
    return df[["ano_mes", "ipca_variacao"]]


def main():
    print("Tratando cotações...")
    cotacoes = tratar_cotacoes()

    print("Tratando Selic...")
    selic = tratar_selic()

    print("Tratando IPCA...")
    ipca = tratar_ipca()

    print("Fazendo merge...")
    resultado = cotacoes.merge(selic, on="ano_mes", how="left")
    resultado = resultado.merge(ipca, on="ano_mes", how="left")

    resultado = resultado[
        ["ano_mes", "ticker", "preco_fechamento", "retorno_mensal_pct", "selic_media", "ipca_variacao"]
    ]
    resultado = resultado.sort_values(["ticker", "ano_mes"]).reset_index(drop=True)

    caminho = os.path.join(PROCESSED_DIR, "dados_tratados.csv")
    resultado.to_csv(caminho, index=False)

    print(f"\nSalvo em {caminho}")
    print("=" * 50)
    print("RESUMO")
    print("=" * 50)
    print(f"Linhas:  {len(resultado)}")
    print(f"Meses:   {resultado['ano_mes'].nunique()}")
    print(f"Tickers: {resultado['ticker'].nunique()}")
    print(f"\nValores nulos por coluna:")
    nulos = resultado.isnull().sum()
    for col, n in nulos.items():
        if n > 0:
            print(f"  {col}: {n}")
    if nulos.sum() == 0:
        print("  Nenhum")


if __name__ == "__main__":
    main()
