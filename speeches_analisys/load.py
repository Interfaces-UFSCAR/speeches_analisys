import pathlib
import pandas as pd
import spacy


def load_speeches_csv(speeches_path: pathlib.Path) -> tuple[list[str],
                                                            list[list[str]]]:
    if not speeches_path.exists():
        raise ValueError("The speeches_path attribute must exist")
    if speeches_path.is_file():
        df_list = [pd.read_csv(speeches_path)]
    else:
        files = speeches_path.iterdir()
        df_list = [pd.read_csv(file) for file in files]
    partidos: list[str] = []
    discursos: list[list[str]] = []
    for df in df_list:
        partidos.extend(df["sigla"].unique().tolist())
    if speeches_path.is_file() and len(partidos) != 1:
        for partido in partidos:
            discursos.append(df_list[0][df_list[0]["sigla"] == partido]["transcricao"].tolist())
    else:
        for df in df_list:
            discursos.append(df["transcricao"].tolist())

    return partidos, discursos


def load_topics_csv(topics_path: pathlib.Path) -> pd.DataFrame:
    df = pd.read_csv(topics_path)
    try:
        df = df.drop("Unnamed: 0", inplace=False, axis=1)
    except KeyError:
        pass
    return df


def load_nlp():
    try:
        nlp = spacy.load("pt_core_news_lg")
    except OSError:
        from spacy.cli import download
        download("pt_core_news_lg")
        nlp = spacy.load("pt_core_news_lg")
    return nlp
