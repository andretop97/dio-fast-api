from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select

from src.contrib.dependencies import DatabaseDependency
from .schema import CentroTreinamento, CentroTreinamentoOut
from .model import CentroTreinamentoModel

router = APIRouter()


@router.post('/', summary="Criar um novo centro de treinamento", status_code=status.HTTP_201_CREATED, response_model= CentroTreinamentoOut)
async def post(db_session: DatabaseDependency, centro_treinamento_in: CentroTreinamento= Body(...)) -> CentroTreinamentoOut:
    centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
    centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())

    db_session.add(centro_treinamento_model)
    await db_session.commit()

    return centro_treinamento_out


@router.get('/', summary="Consultar todos os centros de treinamento", status_code=status.HTTP_200_OK, response_model= list[CentroTreinamentoOut])
async def query(db_session: DatabaseDependency) -> list[CentroTreinamentoOut]:
    centros_treinamento: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()

    return centros_treinamento

@router.get('/{id}', summary="Consultar uma centro de treinamento pelo ID", status_code=status.HTTP_200_OK, response_model= CentroTreinamentoOut)
async def query(id: UUID4,db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro_treinamento: CentroTreinamentoOut = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()

    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Centro de treinamento de id {id} não encontrada')

    return centro_treinamento