"""
Permitir que o usuário interaja com a API do sistema de forma visual,
sem precisar utilizar ferramentas como Postman ou terminal.
"""

import os

import streamlit as st
import requests
import pandas as pd

BASE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "elyndra_database")
)

# URL base da API.
# A API deve estar rodando localmente com FastAPI.
API_URL = "http://127.0.0.1:8000"


# Configuração visual da página
st.set_page_config(
    page_title="Elyndra Game Platform",
    layout="wide"
)


# Título principal da aplicação
st.title("Plataforma de Jogos Elyndra")


if "selected_game" not in st.session_state:
    st.session_state.selected_game = None

if "games_cache" not in st.session_state:
    st.session_state.games_cache = None

def render_game_card(game):

    media = game["media"]

    col1, col2 = st.columns([1,2])

    with col1:

        capa = os.path.join(BASE_PATH, media["capa"].lstrip("/"))

        if os.path.exists(capa):
            st.image(capa)

    with col2:

        st.subheader(game["titulo"])

        st.write(game["descricao_curta"])

        if st.button("Visualizar", key=f"view_{game['_id']}"):
            st.session_state.selected_game = game["_id"]
            st.rerun()

    st.divider()


def render_game_details(game):

    media = game["media"]

    st.header(game["titulo"])

    capa = os.path.join(BASE_PATH, media["capa"].lstrip("/"))
    st.image(capa, width=400)

    st.write(game["descricao"])

    st.subheader("Galeria")

    galeria = [
        os.path.join(BASE_PATH, img.lstrip("/"))
        for img in media["galeria"]
    ]

    st.image(galeria, width=200)

    if media["trailer"]:
        st.subheader("Trailer")
        st.video(media["trailer"][0])

        with st.expander("Requisitos mínimos"):
                        r = game["requisitos"]["minimos"]
                        st.write(f"SO: {r['so']}")
                        st.write(f"CPU: {r['cpu']}")
                        st.write(f"GPU: {r['gpu']}")
                        st.write(f"RAM: {r['ram_gb']} GB")
                        st.write(f"Armazenamento: {r['armazenamento_gb']} GB")

        with st.expander("Requisitos recomendados"):
            r = game["requisitos"]["recomendados"]
            st.write(f"SO: {r['so']}")
            st.write(f"CPU: {r['cpu']}")
            st.write(f"GPU: {r['gpu']}")
            st.write(f"RAM: {r['ram_gb']} GB")
            st.write(f"Armazenamento: {r['armazenamento_gb']} GB")




    if "reviews" in game:

        st.subheader("Reviews")

        for r in game["reviews"]:

            st.write("⭐" * r["nota"])
            st.write(r["comentario"])

            st.divider()
# MENU DE NAVEGAÇÃO


"""
O menu lateral permite navegar entre as funcionalidades da interface.

Cada opção representa uma "página lógica" do sistema.
Dependendo da escolha do usuário, um bloco diferente de código será executado.
"""

menu = st.sidebar.selectbox(
    "Menu de Navegação",
    [
        "Home",
        "Lista de Games",
        "Buscar por Categoria",
        "Média de Avaliações",
        "Usuários",
        "Criar Usuário",
        "Fórum"
    ]
)



#HOME


if menu == "Home":

    st.header("Bem-vindo ao Elyndra")

    st.write("""
    O Elyndra é uma plataforma de gerenciamento de jogos que permite:

    - cadastrar usuários
    - registrar jogos
    - criar reviews
    - participar de discussões em fóruns
    - analisar estatísticas de avaliações

    Esta interface foi desenvolvida com Streamlit para facilitar a interação com o sistema.
    """)


#Listar Jogos


elif menu == "Lista de Games":

    st.header("Lista de Games")

    if st.session_state.selected_game is None:

        games = st.session_state.games_cache

        if games is None:
            response = requests.get(f"{API_URL}/games")
            games = response.json()
            st.session_state.games_cache = games

        for game in games:
            render_game_card(game)

    else:

        game_id = st.session_state.selected_game

        response = requests.get(f"{API_URL}/games/{game_id}")

        if response.status_code == 200:

            game = response.json()

            render_game_details(game)

            if st.button("Voltar"):

                st.session_state.selected_game = None
                st.rerun()



elif menu == "Buscar Games":

    st.header("Buscar Games")

    titulo = st.text_input("Título")

    generos = st.multiselect(
        "Gêneros",
        [
            "RPG",
            "Ação",
            "Aventura",
            "Mundo Aberto"
        ]
    )

    if st.button("Buscar"):

        params = {}

        if titulo:
            params["titulo"] = titulo

        for g in generos:
            params.setdefault("generos", []).append(g)

        response = requests.get(
            f"{API_URL}/games/search",
            params=params
        )

        if response.status_code == 200:

            games = response.json()
            for game in games:
                render_game_card(game)

        else:
            st.error("Erro na busca")


# BUSCAR POR CATEGORIA


elif menu == "Buscar por Categoria":

    st.header("Buscar Jogo por Categoria")

    categoria = st.text_input("Digite a categoria do jogo")

    if st.button("Buscar"):

        response = requests.get(
            f"{API_URL}/games/categoria/{categoria}"
        )

        if response.status_code == 200:

            games = response.json()

            if not games:
                st.warning("Nenhum jogo encontrado")

            for game in games:
                render_game_card(game)

        else:
            st.error("Categoria não encontrada")





#MÉDIA DE AVALIAÇÕES



elif menu == "Média de Avaliações":

    st.header("Média de Avaliações dos Games")

    """
    Esta funcionalidade utiliza uma Aggregation Pipeline do MongoDB
    para calcular a média de avaliações de cada jogo.

    A API executa a agregação e retorna os dados prontos para visualização.
    """

    if st.button("Calcular média das avaliações"):

        response = requests.get(
            f"{API_URL}/analytics/media-avaliacoes"
        )

        if response.status_code == 200:

            dados = response.json()

            df = pd.DataFrame(dados)

            # Exibe tabela com resultados da agregação
            st.dataframe(df)

            # Exibe gráfico de barras com as médias
            st.bar_chart(df["media_avaliacao"])

        else:
            st.error("Erro ao calcular média das avaliações")




# CRIAR USUÁRIO

elif menu == "Usuários":

    st.header("Lista de Usuários")

    # Botão para carregar todos os usuários
    if st.button("Carregar Usuários"):
        response = requests.get(f"{API_URL}/usuarios")
        if response.status_code == 200:
            users = response.json()
            

            # Converte para DataFrame e exibe tudo
            df = pd.DataFrame(users)
            st.dataframe(df)

        else:
            st.error("Erro ao carregar usuários")

elif menu == "Criar Usuário":

    st.header("Criar Novo Usuário")

    """
    Formulário para cadastro de usuário.

    Os dados inseridos são enviados via POST
    para a API FastAPI.
    """

    nome = st.text_input("Nome")
    sobrenome = st.text_input("Sobrenome")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")

    if st.button("Criar Usuário"):

        data = {
            "nome": nome,
            "sobrenome": sobrenome,
            "username": username,
            "email": email,
            "password": password,
            "region": "BR"
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





#FÓRUM



elif menu == "Fórum":

    st.header("Fórum de Discussões")

    response = requests.get(f"{API_URL}/forum")

    if response.status_code == 200:

        posts = response.json()

        for post in posts:

            st.subheader(post["titulo"])

            st.write(post["conteudo"])

            st.write("Tags:", ", ".join(post["tags"]))

            st.write("Respostas")

            for reply in post["replies"]:
                st.write("•", reply["conteudo"])

            st.divider()

    else:
        st.error("Erro ao carregar fórum")