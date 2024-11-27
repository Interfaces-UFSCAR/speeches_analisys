from pydantic import Field
import speeches_scrap.models.baseModel as baseModel


class FaseEvento(baseModel.BaseClass):
    data_hora_fim: str = Field(alias="dataHoraFim")
    data_hora_inicio: str = Field(alias="dataHoraInicio")
    titulo: str = Field(alias="titulo")
