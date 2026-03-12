"""
Permitir que o usuário interaja com a API do sistema de forma visual,
sem precisar utilizar ferramentas como Postman ou terminal.
"""

import streamlit as st
import requests
import pandas as pd

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

    """
    Ao clicar no botão, a interface faz uma requisição GET
    para o endpoint da API que retorna todos os games cadastrados.
    """

    if st.button("Carregar Games"):

        response = requests.get(f"{API_URL}/games")

        if response.status_code == 200:

            # Converte o JSON retornado pela API em uma tabela
            games = response.json()

            df = pd.DataFrame(games)

            # Exibe tabela interativa
            st.dataframe(df)

        else:
            st.error("Erro ao buscar games")





# BUSCAR POR CATEGORIA



elif menu == "Buscar por Categoria":

    st.header("Buscar Jogo por Categoria")

    """
    Permite ao usuário filtrar jogos por categoria.
    O valor digitado é enviado para a API.
    """

    categoria = st.text_input("Digite a categoria do jogo")

    if st.button("Buscar"):

        response = requests.get(
            f"{API_URL}/games/categoria/{categoria}"
        )

        if response.status_code == 200:

            games = response.json()

            df = pd.DataFrame(games)

            st.dataframe(df)

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

    """
    Nesta seção são exibidos os tópicos do fórum do sistema.

    Cada tópico contém:
    - título
    - conteúdo
    - número de upvotes
    """

    if st.button("Carregar tópicos do fórum"):

        response = requests.get(f"{API_URL}/forum")

        if response.status_code == 200:

            posts = response.json()

            for post in posts:

                st.subheader(post["titulo"])

                st.write(post["conteudo"])

                st.write("Upvotes:", post["upvotes"])

                st.write("---")

        else:
            st.error("Erro ao carregar fórum")