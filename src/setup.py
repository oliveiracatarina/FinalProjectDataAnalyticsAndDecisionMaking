import pandas as pd
import numpy as np
from pathlib import Path

## Load FIFA 17 Players CSV file into a DataFrame
arquivo_csv = Path(__file__).parent.parent / "FIFA+17+Players.csv"
df = pd.read_csv(arquivo_csv)

pd.set_option("display.max_columns", 60)

print(df.shape)
df.info()

## Etapa A - Diagnóstico Inicial
n_linhas_antes = len(df)
nulos_antes = df.isna().sum().sum()
duplicatas = df.duplicated().sum()

print("Linhas:", n_linhas_antes)
print("Total de nulos:", nulos_antes)
print("Linhas duplicadas:", duplicatas)
print(df.isna().sum()[df.isna().sum() > 0])

## Etapa B - Limpeza
# 1) Remover duplicatas exatas (ex.: Messi aparece 2x com os mesmos dados)
df = df.drop_duplicates()

# 2) Height e Weight: extrair número
df["Height_cm"] = df["Height"].str.extract(r"(\d+)").astype(float)
df["Weight_kg"] = df["Weight"].str.extract(r"(\d+)").astype(float)

# 3) Datas
df["Birth_Date"] = pd.to_datetime(df["Birth_Date"], format="%m/%d/%Y", errors="coerce")
df["Club_Joining"] = pd.to_datetime(df["Club_Joining"], format="%m/%d/%Y", errors="coerce")

# 4) National_Position nulo não é erro, é "não convocado" -> vira uma coluna própria
df["Convocado_Selecao"] = df["National_Position"].notna()

# 5) Work_Rate: separar em ataque/defesa
work_split = df["Work_Rate"].str.split(" / ", expand=True)
df["WorkRate_Ataque"] = work_split[0]
df["WorkRate_Defesa"] = work_split[1]

# 6) Corrigir nome de colunas com erro de grafia (mantendo rastreabilidade)
df = df.rename(columns={
    "Preffered_Foot": "Preferred_Foot",
    "Preffered_Position": "Preferred_Position_Raw"
})

# 7) Linhas com Nationality nula (só 2) -> avaliar se remove ou marca "Desconhecido"
df["Nationality"] = df["Nationality"].fillna("Desconhecido")
