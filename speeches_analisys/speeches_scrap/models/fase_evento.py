from pydantic import Field
from . import base_model


class FaseEvento(base_model.BaseClass):
    data_hora_fim: str | None = Field(alias="dataHoraFim")
    data_hora_inicio: str | None = Field(alias="dataHoraInicio")
    titulo: str = Field(alias="titulo")
