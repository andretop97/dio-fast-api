from pydantic import UUID4, Field
from typing import Annotated

from src.contrib.schemas import BaseSchema

class CentroTreinamento(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de treinamento", example='Batata Fit', max_length=20)]
    endereco: Annotated[str, Field(description="Endereço do centro de treinamento", example='Batata Fit', max_length=60)]
    proprietario: Annotated[str, Field(description="Proprietario do centro de treinamento", example='Jorge', max_length=30)]


class CentroTreinamentoOut(CentroTreinamento):
    id: Annotated[UUID4, Field(description="Identificador do centro de treinamento")]

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de treinamento", example='Batata Fit', max_length=20)]
