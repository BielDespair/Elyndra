"""
Este módulo implementa um Aggregation Pipeline responsável
por identificar os jogos com as melhores avaliações na plataforma.

A análise considera:

- média das avaliações
- quantidade mínima de reviews (para evitar distorções)

Exemplo:
Um jogo com nota 5 mas apenas 1 review não deve
aparecer acima de um jogo com média 4.8 e 500 reviews.
"""

from ..database import db


def jogos_melhor_avaliados(limit: int = 5, minimo_reviews: int = 3):

    """
    Retorna os jogos com melhor avaliação média.

    Parâmetros
    ----------
    limit : int
        Quantidade máxima de jogos retornados.

    minimo_reviews : int
        Quantidade mínima de reviews necessárias
        para que o jogo entre no ranking.

    Retorno
    -------
    list
        Lista contendo os jogos mais bem avaliados.
    """

    pipeline = [

        # -------------------------------------------------
        # ETAPA 1 — AGRUPAR REVIEWS POR JOGO
        # -------------------------------------------------
        #
        # Cada documento na coleção "reviews"
        # representa uma avaliação feita por um usuário.
        #
        # Agrupamos pelo campo "game_id" para calcular:
        #
        # - média das notas
        # - quantidade total de reviews
        #

        
        {
            "$group": {

                "_id": "$game_id",

                "media_avaliacao": {
                    "$avg": "$nota"
                },

                "total_reviews": {
                    "$sum": 1
                }

            }
        },





        # -------------------------------------------------
        # ETAPA 2 — FILTRAR JOGOS COM POUCAS REVIEWS
        # -------------------------------------------------
        #
        # Remove jogos que possuem poucas avaliações,
        # garantindo que o ranking seja mais confiável.
        #
        {
            "$match": {
                "total_reviews": { "$gte": minimo_reviews }
            }
        },




        # -------------------------------------------------
        # ETAPA 3 — ORDENAR POR MELHOR AVALIAÇÃO
        # -------------------------------------------------
        #
        # Ordenamos primeiro pela média de avaliação
        # e depois pela quantidade de reviews.
        #
        {
            "$sort": {
                "media_avaliacao": -1,
                "total_reviews": -1
            }
        },



        # -------------------------------------------------
        # ETAPA 4 — LIMITAR RESULTADOS
        # -------------------------------------------------
        #
        {
            "$limit": limit
        },

        # -------------------------------------------------
        # ETAPA 5 — BUSCAR INFORMAÇÕES DO JOGO
        # -------------------------------------------------
        #
        # Utilizamos lookup para buscar
        # o título do jogo na coleção "games".
        #
        {
            "$lookup": {

                "from": "games",

                "localField": "_id",

                "foreignField": "_id",

                "as": "game"

            }
        },

        {
            "$unwind": "$game"
        },

        # -------------------------------------------------
        # ETAPA 6 — FORMATAR RESULTADO FINAL
        # -------------------------------------------------
        #
        {
            "$project": {

                "_id": 0,

                "game_id": "$game._id",

                "titulo": "$game.titulo",

                "media_avaliacao": {
                    "$round": ["$media_avaliacao", 2]
                },

                "total_reviews": 1

            }
        }

    ]

    resultado = db["reviews"].aggregate(pipeline)

    return list(resultado)