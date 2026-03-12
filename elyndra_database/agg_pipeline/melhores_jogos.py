"""
Este módulo implementa um pipeline de agregação responsável
por identificar os jogos mais bem avaliados pelos usuários
da plataforma.

Objetivos da análise:

1 - Agrupar reviews por jogo
2 - Calcular a média das avaliações
3 - Contar quantas avaliações cada jogo possui
4 - Ordenar os jogos pela melhor média
5 - Buscar informações do jogo na coleção de jogos
"""

from ..database import db


def jogos_melhor_avaliados(limit: int = 5):

    """
    Retorna um ranking dos jogos com melhor avaliação média.

    Parâmetros
    ----------
    limit : int
        Quantidade máxima de jogos no ranking.

    Retorno
    -------
    list
        Lista com os jogos mais bem avaliados da plataforma.
    """

    pipeline = [



     
        # ETAPA 1 — AGRUPAR REVIEWS POR JOGO
        
        #
        # Agrupamos todas as avaliações pelo campo game_id
        # para calcular estatísticas de cada jogo.
        #
        {
            "$group": {
                "_id": "$game_id",

                # média das avaliações
                "media_avaliacao": {
                    "$avg": "$avaliacao"
                },

                # quantidade de reviews
                "total_reviews": {
                    "$sum": 1
                }
            }
        },




        # -------------------------------------------------
        # ETAPA 2 — FILTRAR JOGOS COM POUCAS AVALIAÇÕES
        # -------------------------------------------------
        #
        # Evita que jogos com apenas 1 avaliação apareçam
        # no topo do ranking.
        #
        {
            "$match": {
                "total_reviews": {
                    "$gte": 3
                }
            }
        },



        # -------------------------------------------------
        # ETAPA 3 — ORDENAR PELOS MELHORES JOGOS
        # -------------------------------------------------
        #
        # Ordena pela maior média de avaliação.
        #
        {
            "$sort": {
                "media_avaliacao": -1
            }
        },



        # -------------------------------------------------
        # ETAPA 4 — LIMITAR RESULTADO
        # -------------------------------------------------
        #
        # Define quantos jogos aparecerão no ranking.
        #
        {
            "$limit": limit
        },



        # -------------------------------------------------
        # ETAPA 5 — BUSCAR INFORMAÇÕES DO JOGO
        # -------------------------------------------------
        #
        # Realiza uma junção com a coleção "games"
        # para obter o título do jogo.
        #
        {
            "$lookup": {
                "from": "games",
                "localField": "_id",
                "foreignField": "_id",
                "as": "game"
            }
        },

        # transforma o array em objeto
        {
            "$unwind": "$game"
        },




        # -------------------------------------------------
        # ETAPA 6 — FORMATAR RESULTADO FINAL
        # -------------------------------------------------
        #
        # Define os campos que aparecerão no ranking.
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