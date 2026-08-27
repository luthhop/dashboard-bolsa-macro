import os

import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

MAPEAMENTO_ATIVOS = {
    "PETR4.SA": ("Petrobras", "Petróleo e Gás"),
    "VALE3.SA": ("Vale", "Mineração"),
    "ITUB4.SA": ("Itaú Unibanco", "Bancário"),
    "WEGE3.SA": ("WEG", "Bens Industriais"),
    "MGLU3.SA": ("Magazine Luiza", "Varejo"),
    "ABEV3.SA": ("Ambev", "Bebidas e Consumo"),
    "CPFE3.SA": ("CPFL Energia", "Energia Elétrica"),
    "^BVSP": ("Ibovespa", "Índice (Benchmark)"),
}


def main():
    df = pd.read_csv(os.path.join(PROCESSED_DIR, "dados_tratados.csv"))

    # dim_ativos
    dim_ativos = pd.DataFrame(
        [(t, e, s) for t, (e, s) in MAPEAMENTO_ATIVOS.items()],
        columns=["ticker", "empresa", "setor"],
    )
    dim_ativos.to_csv(os.path.join(PROCESSED_DIR, "dim_ativos.csv"), index=False)

    # dim_datas
    datas = df[["ano_mes"]].drop_duplicates().sort_values("ano_mes").reset_index(drop=True)
    partes = datas["ano_mes"].str.split("-", expand=True)
    datas["ano"] = partes[0].astype(int)
    datas["mes"] = partes[1].astype(int)
    datas.to_csv(os.path.join(PROCESSED_DIR, "dim_datas.csv"), index=False)

    # fato_retornos
    fato = df[["ano_mes", "ticker", "preco_fechamento", "retorno_mensal_pct", "selic_media", "ipca_variacao"]]
    fato.to_csv(os.path.join(PROCESSED_DIR, "fato_retornos.csv"), index=False)

    for nome, tabela in [("dim_ativos", dim_ativos), ("dim_datas", datas), ("fato_retornos", fato)]:
        print(f"\n{'=' * 50}")
        print(f"{nome}.csv — {len(tabela)} linhas")
        print("=" * 50)
        print(tabela.head().to_string(index=False))


if __name__ == "__main__":
    main()
