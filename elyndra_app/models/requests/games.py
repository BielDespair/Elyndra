from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel

from ..enums import *



class Desconto(BaseModel):
    percentual: float
    valido_ate: datetime

class Preco(BaseModel):
    tipo: TipoPreco
    valor: Decimal
    moeda: Moeda
    desconto: Optional[Desconto]
    
class EspecRequisitos(BaseModel):
    so: str
    cpu: str
    gpu: str
    ram_gb: int
    armazenamento_gb: int
    
class Requisitos(BaseModel):
    minimos: EspecRequisitos
    recomendados: Optional[EspecRequisitos]
    

class Media(BaseModel):
    capa: str
    galeria: List[str] = []
    trailer: List[str] = []

class Features(BaseModel):
    multiplayer: bool = False
    conquistas: bool = True
    suporte_controle: bool = False

class IdiomasSuportados(BaseModel):
    audio: List[Idioma] = []
    legendas: List[Idioma] = []
    interface: List[Idioma] = []
    

class CriarGameRequest(BaseModel):
    titulo: str
    slug: str

    media: Media
    
    estudio: str
    publicadora: str
    data_lancamento: date

    descricao_curta: str
    descricao: str
    
    generos: List[str]
    tags: List[str] = []

    idiomas: IdiomasSuportados
    features: Features
    
    precos: List[Preco]

    
    requisitos: Requisitos
    tamanho_instalacao_mb: int
    tamanho_download_mb: Optional[int]
    
    
    
    status: str = "draft"
    visibilidade: str = "private"