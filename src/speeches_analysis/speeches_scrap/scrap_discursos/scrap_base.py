import time
import requests


def req_url(s: requests.Session,
            url: str,
            try_times: int = 10) -> requests.Response:
    """Requests a certain URL using the given Session thais is being used.
    O ptional parameter to set how many times will try to scrape"""
    _not_got = True
    times = 0
    while _not_got and times < try_times:
        response = s.get(url)
        if response.status_code >= 200 and response.status_code < 300:
            _not_got = False
        elif response.status_code == 429:
            retry_after = int(response.headers["retry-after"])
            time.sleep(retry_after)
    return response


def create_params(id_legislatura: list[str] | None = None,
                  data_inicio: str = "",
                  data_fim: str = "",
                  ordenar_por: str = "",
                  ordem: str = "") -> dict[str, str | list[str]]:
    params: dict[str, str | list[str]] = {}
    if (id_legislatura != []) and (id_legislatura is not None):
        params["idLegislatura"] = [str(legislatura)
                                   for legislatura in id_legislatura]
    if data_inicio != "":
        params["dataInicio"] = data_inicio
    if data_fim != "":
        params["dataFim"] = data_fim
    if ordenar_por != "":
        params["ordenarPor"] = ordenar_por
    params["ordem"] = ordem
    return params
