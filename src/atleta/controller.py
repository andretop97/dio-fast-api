from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select
from fastapi_pagination import LimitOffsetPage, paginate

from src.categorias.model import CategoriaModel
from src.categorias.schemas import CategoriaOut
from src.centro_treinamento.model import CentroTreinamentoModel
from src.centro_treinamento.schema import CentroTreinamentoOut
from src.contrib.dependencies import DatabaseDependency
from .schemas import Atleta, AtletaOut, AtletaUpdate, AtletaList
from .model import AtletaModel

router = APIRouter()

@router.post('/', summary="Criar novo atleta", status_code=status.HTTP_201_CREATED, response_model=AtletaOut)
async def post(db_session: DatabaseDependency, atleta_in: Atleta= Body(...)):
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome
    atleta_cpf = atleta_in.cpf

    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(cpf=atleta_cpf))).scalars().first()

    if atleta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= f'Atleta de cpf {atleta_cpf} ja cadastrado'
            ) 

    categoria: CategoriaOut = (await db_session.execute(
        select(CategoriaModel).filter_by(nome=categoria_nome)
        )).scalars().first()
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= f'Categoria {categoria_nome} não foi encontrada'
            )
    
    centro_treinamento: CentroTreinamentoOut = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome)
        )).scalars().first()
    
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= f'O centro de treinamento {centro_treinamento_nome} não foi encontrada'
            )

    try:

        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.now(), updated_at=datetime.now(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= f'Ocorreu um erro ao inserir os dados no banco'
            )

    return atleta_model

@router.get('/', summary="Consultar todos os atletas", status_code=status.HTTP_200_OK, response_model= LimitOffsetPage[AtletaList])
async def query(db_session: DatabaseDependency, nome: str = None, cpf: str = None) -> LimitOffsetPage[AtletaList]:
    atletas: list[AtletaList] = (await db_session.execute(select(AtletaModel))).scalars().all()

    if nome:
        atletas = [atleta for atleta in atletas if atleta.nome == nome]

    if cpf:
        atletas = [atleta for atleta in atletas if atleta.cpf == cpf]

    return paginate([AtletaList.model_validate(atleta) for atleta in atletas])

@router.get('/{id}', summary="Consultar uma atleta pelo ID", status_code=status.HTTP_200_OK, response_model= AtletaOut)
async def query(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta de id {id} não encontrada')

    return atleta

@router.patch('/{id}', summary="Editar uma atleta pelo ID", status_code=status.HTTP_200_OK, response_model= AtletaOut, )
async def query(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate= Body(...)) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta de id {id} não encontrada')

    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta

@router.delete('/{id}', summary="Editar uma atleta pelo ID", status_code=status.HTTP_204_NO_CONTENT)
async def query(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate= Body(...)) -> None:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta de id {id} não encontrada')

    await db_session.delete(atleta)
    await db_session.commit()
    
    return atleta