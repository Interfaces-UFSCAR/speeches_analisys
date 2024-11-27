import pandas as pd

from speeches_analisys.speeches_scrap.models import partido as model_partido
from speeches_analisys.speeches_scrap.models import deputado as model_deputado
from speeches_analisys.speeches_scrap.models import discurso as model_discurso


def to_dataframe(structure: dict[model_partido.Partido,
                                 dict[model_deputado.Deputado,
                                      list[model_discurso.Discurso]
                                      ]
                                 ]) -> pd.DataFrame:
    list_df = []
    for partido, deputados_dict in structure.items():
        for deputado, discursos_list in deputados_dict.items():
            for discurso in discursos_list:
                partido_list = partido.to_list()
                deputado_list = deputado.to_list()
                discurso_list = discurso.to_list()
                linha = partido_list + deputado_list + discurso_list
                list_df.append(linha)

    columns = model_partido.Partido.get_variables() + \
        model_deputado.Deputado.get_variables() + \
        model_discurso.Discurso.get_variables()
    df = pd.DataFrame(data=list_df, columns=columns)
    df = df.drop_duplicates(subset=["dataHoraFim",
                                    "dataHoraInicio",
                                    "faseVento.dataHoraFim",
                                    "faseEvento.dataHoraInicio",
                                    "faseEvento.titulo",
                                    "keywords",
                                    "sumario",
                                    "tipoDiscurso",
                                    "transcricao",
                                    "uriEvento",
                                    "urlAudio",
                                    "urlTexto",
                                    "urlVideo"])
    return df
