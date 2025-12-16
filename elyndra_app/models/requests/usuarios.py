from pydantic import BaseModel
from ..enums import Region


class CriarUsuario(BaseModel):
    nome: str
    sobrenome: str
    
    username: str
    
    region: Region
    
    # Login
    email: str
    password: str
    
    
    
