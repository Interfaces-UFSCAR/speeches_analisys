from pydantic import Field
from . import baseModel


class FaseEvento(baseModel.BaseClass):
    data_hora_fim: str | None = Field(alias="dataHoraFim")
    data_hora_inicio: str | None = Field(alias="dataHoraInicio")
    titulo: str = Field(alias="titulo")
