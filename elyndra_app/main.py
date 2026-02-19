from fastapi import FastAPI, HTTPException, status
from .models.requests import *
from elyndra_database.connection import get_database
from elyndra_database.repositorios.user_repository import UserRepository
from elyndra_database.bootstrap.indexes import create_indexes

from elyndra_database.bootstrap import (
    seed_usuarios,
    seed_games,
    seed_biblioteca,
    seed_reviews,
    seed_forum
)

from elyndra_database.database import client
from elyndra_database.bootstrap import DROP_DATABASE



app = FastAPI()
db = get_database()
user_repo = UserRepository(db)

@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/usuarios/{id}")
async def get_usuario(id: int):
    usuario = user_repo.get(id)
    
    if (usuario is None):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return usuario
    
@app.post("/usuarios")
async def criar_usuario(usuario: CriarUsuario):

    # Verificar se email já existe no banco

    if user_repo.find_by_email(usuario.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este e-mail já está cadastrado!"
        )

    result = usuario.model_dump()


    return {
        "message": "Usuário criado com sucesso",
        "id": str(result.inserted_id)
    }


@app.post("/games")
async def criar_game(game: CriarGameRequest):
    
    return {"message": "Game criado com sucesso!"}


@app.get("/games/{id}")
async def get_game(id: int):
    return {"message": f"Detalhes do game com id {id}"}


def main():
    if DROP_DATABASE:
        client.drop_database("elyndra")

    seed_usuarios(db)
    seed_games(db)
    seed_biblioteca(db)
    seed_reviews(db)
    seed_forum(db)

    create_indexes(db)

