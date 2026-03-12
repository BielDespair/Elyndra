import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Plataforma de Jogos Elyndra")

menu = st.sidebar.selectbox(
    "Menu",
    ["Home", "Buscar Game", "Criar Usuário"]
)



#Página Principal 


if menu == "Home":
    st.header("Bem-vindo ao Elyndra")
    st.write("Plataforma de games com biblioteca, reviews e fórum.")



#Buscar Jogo

elif menu == "Buscar Game":
    st.header("Buscar Game")

    game_id = st.text_input("ID do Game")

    if st.button("Buscar"):
        response = requests.get(f"{API_URL}/games/{game_id}")

        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error("Game não encontrado")




#Criar Usuário

elif menu == "Criar Usuário":

    st.header("Criar novo usuário")

    username = st.text_input("Username")
    email = st.text_input("Email")

    if st.button("Criar usuário"):

        data = {
            "username": username,
            "email": email
        }

        response = requests.post(
            f"{API_URL}/usuarios",
            json=data
        )

        if response.status_code == 200:
            st.success("Usuário criado com sucesso")
            st.json(response.json())
        else:
            st.error(response.text)

            