from fastapi import APIRouter

from .atleta.controller import router as atletas
from .categorias.controller import router as categorias
from .centro_treinamento.controller import router as centros_treinamento
api_router = APIRouter()

api_router.include_router(atletas, prefix='/atletas', tags=['atletas'])
api_router.include_router(categorias, prefix='/categorias', tags=['categorias'])
api_router.include_router(centros_treinamento, prefix='/centros_treinamento', tags=['centros_treinamento'])

