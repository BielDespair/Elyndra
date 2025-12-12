from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI()

class Usuario (BaseModel):
     nome: str
     email: str
     idade: int

usuarios = ["Ana", "Jena", "Wendel"]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/usuarios")
async def listar_usuarios():
    return usuarios

@app.post("/usuarios")
async def criar_usuario( usuario: Usuario):
    usuarios.append(usuario)
    print(usuarios)
    return True 


