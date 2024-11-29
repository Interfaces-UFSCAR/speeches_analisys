"""
This module implements the necessary methods to retrieve data based on a party
"""

import urllib.parse
import requests
from pydantic_core import from_json
from requests.structures import CaseInsensitiveDict

from speeches_analisys.speeches_scrap.models import partido

from speeches_analisys.speeches_scrap.scrap_discursos import scrap_base as base
from speeches_analisys.speeches_scrap.scrap_discursos import deputados


def __req_partido(s: requests.Session,
                  url: str) -> list[partido.Partido]:
    """Requests a list of parties from the API.
    Parameters:
        s: A session object which will be used to access the API;
        url: The URL to start the first request.
    Response:
        partidos: A list of Party obects with the recovered data."""
    resps: list[requests.Response] = []
    response = base.req_url(s=s, url=url)
    resps.append(response)
    while "next" in response.links:
        url = response.links["next"]["url"]
        response = base.req_url(s=s, url=url)
        resps.append(response)
    partidos: list[partido.Partido] = []
    for resp in resps:
        partidos.extend(list(map(partido.Partido.model_validate,
                                 from_json(resp.content)["dados"])))
    return partidos


def req_partidos(siglas: list[str] | None = None,
                 data_inicio: str = "",
                 data_fim: str = "",
                 id_legislatura: list[str] | None = None,
                 ordem: str = "ASC",
                 ordenar_por: str = "sigla",
                 ordenar_por_discursos: str = ""
                 ):
    """
    Retrieves the parties based on the list of siglas.
    Enable configuration of the search based on the date, the legislature ID.
    """
    if siglas is None:
        siglas = []
    if id_legislatura is None:
        id_legislatura = []
    discursos_deputados_partidos: dict[partido.Partido, dict]
    url_list = []
    url_base = "https://dadosabertos.camara.leg.br/api/v2/partidos"
    url_list.append(url_base)

    params: dict[str, str | list[str]] = base.create_params(
        id_legislatura=id_legislatura,
        data_inicio=data_inicio,
        data_fim=data_fim,
        ordenar_por=ordenar_por,
        ordem=ordem
    )
    params_copy = params.copy()
    if siglas != []:
        params["sigla"] = siglas
    query = urllib.parse.urlencode(params, doseq=True)
    url_list.append("?")
    url_list.append(query)
    url = "".join(url_list)

    headers: CaseInsensitiveDict[str] = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    s = requests.Session()
    s.headers.update(headers)

    partidos = __req_partido(s=s, url=url)

    discursos_deputados_partidos = {
        __partido: deputados.req_deputados(
            id_partido=__partido.Id,
            s=s,
            params=params_copy,
            ordenar_por=ordenar_por_discursos
        )
        for __partido in partidos
    }
    return discursos_deputados_partidos
