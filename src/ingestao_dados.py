import os
from datetime import datetime, timedelta

import pandas as pd
import requests
import yfinance as yf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

TICKERS = [
    "PETR4.SA",
    "VALE3.SA",
    "ITUB4.SA",
    "WEGE3.SA",
    "MGLU3.SA",
    "ABEV3.SA",
    "CPFE3.SA",
    "^BVSP",
]

SERIES_BCB = {
    "selic": 432,
    "ipca": 433,
}

DATA_FIM = datetime.today()
DATA_INICIO = DATA_FIM - timedelta(days=5 * 365)


def baixar_cotacoes():
    print("=" * 60)
    print("BAIXANDO COTAÇÕES VIA YFINANCE")
    print("=" * 60)

    frames = []
    falhas = []

    for ticker in TICKERS:
        print(f"  Baixando {ticker}...", end=" ")
        try:
            df = yf.download(
                ticker,
                start=DATA_INICIO.strftime("%Y-%m-%d"),
                end=DATA_FIM.strftime("%Y-%m-%d"),
                progress=False,
                auto_adjust=True,
            )
            if df.empty:
                print("SEM DADOS")
                falhas.append(ticker)
                continue

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel(1)

            df = df.reset_index()
            df["Ticker"] = ticker
            frames.append(df)
            print(f"OK — {len(df)} linhas ({df['Date'].min().date()} a {df['Date'].max().date()})")
        except Exception as e:
            print(f"ERRO: {e}")
            falhas.append(ticker)

    if frames:
        cotacoes = pd.concat(frames, ignore_index=True)
        caminho = os.path.join(RAW_DIR, "cotacoes_acoes.csv")
        cotacoes.to_csv(caminho, index=False)
        print(f"\n  Salvo em {caminho}")
        print(f"  Total: {len(cotacoes)} linhas, {cotacoes['Ticker'].nunique()} tickers")
    else:
        print("\n  Nenhuma cotação baixada!")

    if falhas:
        print(f"  FALHAS: {', '.join(falhas)}")

    return falhas


def baixar_serie_bcb(nome, codigo):
    print(f"  Baixando {nome.upper()} (série {codigo})...", end=" ")

    dt_inicio = DATA_INICIO.strftime("%d/%m/%Y")
    dt_fim = DATA_FIM.strftime("%d/%m/%Y")
    url = (
        f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
        f"?formato=json&dataInicial={dt_inicio}&dataFinal={dt_fim}"
    )

    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    dados = resp.json()

    df = pd.DataFrame(dados)
    df["data"] = pd.to_datetime(df["data"], dayfirst=True)
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")

    caminho = os.path.join(RAW_DIR, f"{nome}.csv")
    df.to_csv(caminho, index=False)
    print(f"OK — {len(df)} linhas ({df['data'].min().date()} a {df['data'].max().date()})")
    print(f"  Salvo em {caminho}")


def baixar_macro():
    print("\n" + "=" * 60)
    print("BAIXANDO SÉRIES MACROECONÔMICAS (API BCB)")
    print("=" * 60)

    for nome, codigo in SERIES_BCB.items():
        try:
            baixar_serie_bcb(nome, codigo)
        except Exception as e:
            print(f"ERRO: {e}")


def main():
    print(f"Período: {DATA_INICIO.date()} a {DATA_FIM.date()}\n")
    baixar_cotacoes()
    baixar_macro()
    print("\n" + "=" * 60)
    print("INGESTÃO CONCLUÍDA")
    print("=" * 60)


if __name__ == "__main__":
    main()
