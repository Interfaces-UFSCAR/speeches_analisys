import requests
import urllib.parse
from pydantic_core import from_json

import speeches_analisys.speeches_scrap.models.discurso as discurso

from speeches_analisys.speeches_scrap.scrap_discursos import scrap_base as base


def req_discursos(deputado: int,
                  s: requests.Session,
                  params: dict[str, str | list[str]],
                  ordenar_por: str = "dataHoraInicio"
                  ) -> list[discurso.Discurso]:
    url_list = []
    resps: list[requests.Response] = []
    url_base = "https://dadosabertos.camara.leg.br/api/v2/deputados/{id}/discursos"
    url_list.append(url_base)

    params["ordenarPor"] = ordenar_por
    query = urllib.parse.urlencode(params, doseq=True)
    url_list.append("?")
    url_list.append(query)
    url_id = ''.join(url_list)

    url = url_id.format(id=deputado)
    i = 0
    response = base.req_url(s=s, url=url)
    resps.append(response)

    while "next" in resps[i].links:
        url = resps[i].links["next"]["url"]
        response = base.req_url(s=s, url=url)
        resps.append(response)
        i += 1
    lista_discursos: list[discurso.Discurso] = []
    for resp in resps:
        lista_discursos.extend(list(
            map(discurso.Discurso.model_validate,
                from_json(resp.content)["dados"]))
                )

    return lista_discursos
