import pathlib
import pandas as pd


def load_speeches(speeches_path: pathlib.Path):
    if speeches_path is str:
        speeches_path = pathlib.Path(speeches_path)
    if not speeches_path.exists():
        raise ValueError("The speeches_path attribute must exist")
    if speeches_path.is_file():
        df_list = [pd.read_csv(speeches_path)]
    else:
        files = speeches_path.iterdir()
        df_list = [pd.read_csv(file) for file in files]
    partidos = []
    discursos = []
    for df in df_list:
        partidos.extend(df["sigla"].unique().tolist())
        discursos.append(df["transcricao"].tolist())

    return partidos, discursos
