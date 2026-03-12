from fastapi import FastAPI, HTTPException, Response, status

from elyndra_database.agg_pipeline.categoria_mais_popular import categorias_mais_populares
from elyndra_database.forum.get_forum_posts import get_forum_posts_repo
from elyndra_database.games.get_game_by_id import get_game_by_id
from elyndra_database.games.search_games import get_games_by_category_repo
from elyndra_database.usuarios.create_usuario import create_usuario_repo
from elyndra_database.usuarios.get_usuario_by_id import get_usuario_repo
from elyndra_database.usuarios.listar_usuarios import listar_usuarios_repo
from .models.requests import *
from elyndra_database.connection import get_database
from elyndra_database.repositorios.user_repository import UserRepository
from elyndra_database.games.get_games import get_games


app = FastAPI()
db = get_database()
user_repo = UserRepository(db)

@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/usuarios")
async def get_usuarios():
    return Response(content=listar_usuarios_repo(), media_type="application/json")
    
@app.get("/usuarios/{id}")
async def get_usuario(id: str):
    usuario = get_usuario_repo(id)
    
    if (usuario is None):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return usuario
    
@app.post("/usuarios")
async def criar_usuario(usuario: CriarUsuario):
    # verificação de email
    if user_repo.find_by_email(usuario.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este e-mail já está cadastrado!"
        )

    usuario_dict = usuario.model_dump()
    usuario_id = create_usuario_repo(usuario_dict)

    return {
        "message": "Usuário criado com sucesso",
        "id": usuario_id
    }

@app.post("/games")
async def criar_game(game: CriarGameRequest):
    
    return {"message": "Game criado com sucesso!"}


@app.get("/games/{id}")
async def get_game(id: str):
    return get_game_by_id(id)

@app.get("/games")
async def listar_games():
    return get_games()


@app.get("/games/categoria/{category}")
async def get_games_categoria(category: str):
    return get_games_by_category_repo(category)

@app.get("/forum")
def list_forum():

    posts = get_forum_posts_repo()

    return posts

@app.get("/categorias")
def list_forum():

    categorias = categorias_mais_populares(10)
    print(categorias)

    return categorias