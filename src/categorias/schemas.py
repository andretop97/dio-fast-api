from pydantic import Field, UUID4
from typing import Annotated

from src.contrib.schemas import BaseSchema

class Categoria(BaseSchema):
    nome: Annotated[str, Field(description="Nome da categoria", example='Scale', max_length=10)]

class CategoriaOut(Categoria):
    id: Annotated[UUID4, Field(description="Identificador da categoria")]