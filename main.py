import uuid
from datetime import date, datetime
from enum import Enum
from typing import List, Optional
from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(
    title="Galera do Vôlei API - Especificação",
    description="Especificação da API para gerenciamento de partidas e jogadores de vôlei.",
    version="1.0.0",
)

class Sexo(str, Enum): MASCULINO = "MASCULINO"; FEMININO = "FEMININO"
class CategoriaPartida(str, Enum): INICIANTE = "INICIANTE"; AMADOR = "AMADOR"; INTERMEDIARIO = "INTERMEDIARIO"; AVANCADO = "AVANCADO"; PROFISSIONAL = "PROFISSIONAL"
class TipoPartida(str, Enum): MISTA = "MISTA"; MASCULINA = "MASCULINA"; FEMININA = "FEMININA"
class StatusPartida(str, Enum): AGENDADA = "AGENDADA"; EM_ADESAO = "EM_ADESAO"; COMPLETA = "COMPLETA"; REALIZADA = "REALIZADA"; CANCELADA = "CANCELADA"
class JogadorBase(BaseModel): nome: str = Field(..., min_length=3); email: EmailStr; data_nascimento: date; sexo: Sexo; categoria: CategoriaPartida
class JogadorCreate(JogadorBase): senha: str = Field(..., min_length=8)
class Jogador(JogadorBase): id: uuid.UUID
class PartidaBase(BaseModel): local_descricao: str; data_hora: datetime; categoria: CategoriaPartida; tipo: TipoPartida
class PartidaCreate(PartidaBase): owner_id: uuid.UUID
class Partida(PartidaBase): id: uuid.UUID; owner_id: uuid.UUID; status: StatusPartida; jogadores_confirmados: List[uuid.UUID] = []; jogadores_pendentes: List[uuid.UUID] = []
class SolicitacaoAdesao(BaseModel): jogador_id: uuid.UUID
class AprovacaoJogador(BaseModel): owner_id: uuid.UUID; jogador_id_aprovar: uuid.UUID

@app.post("/jogadores", response_model=Jogador, status_code=status.HTTP_201_CREATED, tags=["Jogadores"])
def criar_jogador(jogador_data: JogadorCreate):
    return Jogador(id=uuid.uuid4(), **jogador_data.dict(exclude={"senha"}))

@app.get("/jogadores/{jogador_id}", response_model=Jogador, tags=["Jogadores"])
def obter_jogador(jogador_id: uuid.UUID):
    return Jogador(id=jogador_id, nome="Jogador", email="jogador@exemplo.com", data_nascimento=date(2000, 1, 1), sexo=Sexo.MASCULINO, categoria=CategoriaPartida.AMADOR)

@app.post("/partidas", response_model=Partida, status_code=status.HTTP_201_CREATED, tags=["Partidas"])
def agendar_partida(partida_data: PartidaCreate):
    return Partida(id=uuid.uuid4(), status=StatusPartida.EM_ADESAO, **partida_data.dict())

@app.get("/partidas", response_model=List[Partida], tags=["Partidas"])
def listar_partidas(categoria: Optional[CategoriaPartida] = None, tipo: Optional[TipoPartida] = None, status: Optional[StatusPartida] = None):
    return []

@app.get("/partidas/{partida_id}", response_model=Partida, tags=["Partidas"])
def obter_partida(partida_id: uuid.UUID):
    return Partida(id=partida_id, owner_id=uuid.uuid4(), local_descricao="Local", data_hora=datetime.now(), categoria=CategoriaPartida.MISTA, tipo=TipoPartida.MISTA, status=StatusPartida.EM_ADESAO)

@app.post("/partidas/{partida_id}/solicitar-adesao", status_code=status.HTTP_200_OK, tags=["Ações em Partidas"])
def solicitar_adesao_partida(partida_id: uuid.UUID, solicitacao: SolicitacaoAdesao):
    return {"message": "Operação registrada."}

@app.post("/partidas/{partida_id}/aprovar-jogador", response_model=Partida, tags=["Ações em Partidas"])
def aprovar_jogador_partida(partida_id: uuid.UUID, aprovacao: AprovacaoJogador):
    return obter_partida(partida_id)

@app.post("/partidas/{partida_id}/cancelar", response_model=Partida, tags=["Ações em Partidas"])
def cancelar_partida(partida_id: uuid.UUID):
    partida_mock = obter_partida(partida_id)
    partida_mock.status = StatusPartida.CANCELADA
    return partida_mock

@app.post("/partidas/{partida_id}/finalizar", response_model=Partida, tags=["Ações em Partidas"])
def finalizar_partida(partida_id: uuid.UUID):
    partida_mock = obter_partida(partida_id)
    partida_mock.status = StatusPartida.REALIZADA
    return partida_mock

@app.post("/partidas/{partida_id}/fechar-adesao", response_model=Partida, tags=["Ações em Partidas"])
def fechar_adesao_partida(partida_id: uuid.UUID):
    partida_mock = obter_partida(partida_id)
    partida_mock.status = StatusPartida.COMPLETA
    return partida_mock
