"""
Elyndra - Analise Estatística de Avaliações de Jogos
Este módulo contém pipelines de agregação utilizados para gerar
estatísticas sobre os jogos da plataforma Elyndra.
"""

from pymongo.database import Database

# FUNÇÃO PRINCIPAL

def calcular_media_avaliacoes(db: Database):

    """
    Executa uma agregação na coleção 'reviews'
    para calcular estatísticas de avaliação dos jogos.

    Parâmetro

    db : Database
        Conexão ativa com o banco MongoDB.


    Retorno

    list
        Lista contendo documentos com estatísticas
        de avaliação por jogo.
    """

    
    # PIPELINE DE AGREGAÇÃO

    pipeline = [

        #FILTRAGEM DE REVIEWS VISÍVEIS
       
        #
        # Nesta etapa utilizamos $match para selecionar
        # apenas reviews válidas que devem participar
        # das estatísticas.
        #

        # Isso evita considerar:
        # - reviews ocultas
        # - reviews denunciadas
        #
        {
            "$match": {
                "visivel": True,
                "denuncias": False
            }
        },



        #AGRUPAMENTO POR JOGO
        # -------------------------------------------------
        #
        # Aqui agrupamos todas as reviews pelo campo game_id.
        #
        # Para cada jogo calculamos:
        #
        # média das avaliações
        # total de reviews
        #
        {
            "$group": {

                # campo que define o agrupamento
                "_id": "$game_id",

                # média das avaliações
                "media_avaliacao": {
                    "$avg": "$avaliacao"
                },

                # total de reviews do jogo
                "total_reviews": {
                    "$sum": 1
                }

            }
        },

        # -------------------------------------------------


        #JUNÇÃO COM COLEÇÃO DE GAMES
        # -------------------------------------------------
        
        #
        # Utilizamos $lookup para buscar informações
        # adicionais do jogo na coleção 'games'.
        #
        # Isso funciona de forma semelhante a um JOIN no SQL.
        #

        {
            "$lookup": {
                "from": "games",
                "localField": "_id",
                "foreignField": "_id",
                "as": "game"
            }
        },




        # -------------------------------------------------
        #DESNORMALIZAÇÃO DO RESULTADO
        # -------------------------------------------------
        #
        # O $lookup retorna um array.
        # Como cada jogo possui apenas um documento,
        # utilizamos $unwind para transformar o array
        # em um objeto simples.
        #
        {
            "$unwind": "$game"
        },

        # -------------------------------------------------




        #PROJEÇÃO DOS CAMPOS FINAIS

        # -------------------------------------------------
        #
        # Aqui definimos quais campos devem aparecer
        # no resultado final da agregação.
        #
        {
            "$project": {

                # removemos o _id original
                "_id": 0,

                # id do jogo
                "game_id": "$game._id",

                # nome do jogo
                "nome_game": "$game.nome",

                # categoria do jogo
                "categoria": "$game.categoria",

                # média calculada
                "media_avaliacao": 1,

                # total de reviews
                "total_reviews": 1
            }
        },




        # -------------------------------------------------
        #ORDENAÇÃO DOS RESULTADOS
        # -------------------------------------------------
        #
        # Ordenamos os jogos pela maior média de avaliação.
        #
        {
            "$sort": {
                "media_avaliacao": -1
            }
        }

    ]






    # EXECUÇÃO DO PIPELINE

    result = db["reviews"].aggregate(pipeline)

    # convertendo cursor para lista
    return list(result)