from pydantic import Field
from . import baseModel


class FaseEvento(baseModel.BaseClass):
    data_hora_fim: str = Field(alias="dataHoraFim")
    data_hora_inicio: str = Field(alias="dataHoraInicio")
    titulo: str = Field(alias="titulo")
