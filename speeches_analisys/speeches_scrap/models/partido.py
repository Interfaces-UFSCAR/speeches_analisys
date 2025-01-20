from pydantic import Field
from . import base_model


class Partido(base_model.BaseClass):
    """This class represents a party"""
    Id: int = Field(alias="id")
    sigla: str = Field(alias="sigla")
    nome: str = Field(alias="nome")
    uri: str = Field(alias="uri")

    def to_list(self) -> list[str | int]:
        "Returns a list from the object Partido"
        return [self.Id, self.sigla, self.nome, self.uri]

    @classmethod
    def get_variables(cls):
        '''Returns a list of names for the Partidos attributes'''
        return ["IdPartido", "sigla", "nome", "uri"]
