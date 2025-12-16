from pydantic import BaseModel




class IniciarSessaoRequest(BaseModel):
    user_id: str
    game_id: str
    
    
    
    
class FinalizarSessaoRequest(BaseModel):
    user_id: str
    game_id: str