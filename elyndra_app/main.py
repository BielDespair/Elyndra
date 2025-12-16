from fastapi import FastAPI, HTTPException, Response, status
from .models.requests import *

usuarios = {}


app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/usuarios/{id}")
async def get_usuario(id: int):
    usuario = usuarios.get(id)
    
    if (usuario is None):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return usuario
    
@app.post("/usuarios")
async def get_usuarios(usuario: CriarUsuario):
    
    print(usuarios)
    if any(u["email"] == usuario.email for u in usuarios.values()):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Este e-mail já está cadastrado!")
        
    id = max(usuarios.keys(), default=0) + 1
    
    usuarios[id] = {
        "nome" : usuario.nome,
        "sobrenome": usuario.sobrenome,
        "username": usuario.username,
        "region": usuario.region,
        "email": usuario.email,
        "password": usuario.password
    }
    
    return Response(status_code=status.HTTP_201_CREATED)



@app.post("/games")
async def criar_game(game: CriarGameRequest):
    
    return {"message": "Game criado com sucesso!"}


@app.get("/games/{id}")
async def get_game(id: int):
    return {"message": f"Detalhes do game com id {id}"}
