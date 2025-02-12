import requests
import urllib.parse
from pydantic_core import from_json

from speeches_analisys.speeches_scrap.models import deputado

from speeches_analisys.speeches_scrap.scrap_discursos import scrap_base as base
from speeches_analisys.speeches_scrap.scrap_discursos import discursos


def req_deputados(id_partido: int,
                  s: requests.Session,
                  params: dict[str, str | list[str]],
                  ordenar_por: str = ""):
    discursos_deputados: dict[deputado.Deputado,
                              list[discursos.discurso.Discurso]]
    url_list = []
    url_base = "https://dadosabertos.camara.leg.br/api/v2/partidos/{id}/membros"
    url_list.append(url_base)

    params["ordenarPor"] = ordenar_por

    query = urllib.parse.urlencode(params, doseq=True)
    url_list.append("?")
    url_list.append(query)
    url_id = ''.join(url_list)
    url = url_id.format(id=id_partido)

    response = base.req_url(s=s, url=url)

    lista_deputados = list(map(deputado.Deputado.model_validate,
                               from_json(response.content)["dados"]))

    discursos_deputados = {deputado_:
                           discursos.req_discursos(deputado=deputado_.Id,
                                                   s=s,
                                                   params=params.copy(),
                                                   ordenar_por=ordenar_por)
                           for deputado_ in lista_deputados}
    return discursos_deputados
