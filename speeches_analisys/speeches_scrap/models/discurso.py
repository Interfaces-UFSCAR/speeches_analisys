from pydantic import Field
from . import base_model
from .fase_evento import FaseEvento


class Discurso(base_model.BaseClass):
    data_hora_fim: str | None = Field(alias="dataHoraFim")
    data_hora_inicio: str = Field(alias="dataHoraInicio")
    fase_evento: FaseEvento = Field(alias="faseEvento")
    keywords: str | None = Field(alias="keywords")
    sumario: str | None = Field(alias="sumario")
    tipo_discurso: str | None = Field(alias="tipoDiscurso")
    transcricao: str = Field(alias="transcricao")
    uri_evento: str | None = Field(alias="uriEvento")
    url_audio: str | None = Field(alias="urlAudio")
    url_texto: str | None = Field(alias="urlTexto")
    url_video: str | None = Field(alias="urlVideo")

    def to_list(self):
        return [self.data_hora_fim,
                self.data_hora_inicio,
                self.fase_evento.data_hora_fim,
                self.fase_evento.data_hora_inicio,
                self.fase_evento.titulo,
                self.keywords,
                self.sumario,
                self.tipo_discurso,
                self.transcricao,
                self.uri_evento,
                self.url_audio,
                self.url_texto,
                self.url_video]

    @classmethod
    def get_variables(cls):
        '''Returns a list of names for the Discurso class.
        To obtain the attributes themselves, use the to_list method.'''
        return ["dataHoraFim",
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
                "urlVideo"]
