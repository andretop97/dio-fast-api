from typing import Annotated, Optional
from pydantic import Field, PositiveFloat

from src.categorias.schemas import Categoria
from src.centro_treinamento.schema import CentroTreinamentoAtleta
from src.contrib.schemas import BaseSchema
from src.contrib.schemas import OutMixin

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", example="Andre", max_length=50)]
    cpf: Annotated[str, Field(description="CPF do atleta", example='12345678900', max_length=11)]
    idade: Annotated[int, Field(description="Idade do atleta", example=26)]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta", example=88.5)]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta", example=1.76)]
    sexo: Annotated[str, Field(description="Sexo do atleta", example="M")]
    categoria: Annotated[Categoria, Field(description="Categoria do atleta")]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description="Centro de treinamento do atleta")]

class AtletaIn(Atleta):
    pass

class AtletaOut(Atleta, OutMixin):
    pass

class AtletaUpdate(Atleta, OutMixin):
    nome: Annotated[Optional[str], Field(None, description="Nome do atleta", example="Andre", max_length=50)]
    idade: Annotated[Optional[int], Field(None, description="Idade do atleta", example=26)]
    peso: Annotated[Optional[PositiveFloat], Field(None, description="Peso do atleta", example=88.5)]
    altura: Annotated[Optional[PositiveFloat], Field(None, description="Altura do atleta", example=1.76)]

class AtletaList(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", example="Andre", max_length=50)]
    categoria: Annotated[Categoria, Field(description="Categoria do atleta")]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description="Centro de treinamento do atleta")]