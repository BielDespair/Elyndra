"""
Este módulo implementa um Aggregation Pipeline responsável
por calcular o tempo médio jogado por usuário em cada jogo.

Essa análise permite identificar quais jogos possuem maior
nível de engajamento dentro da plataforma.

Objetivos da análise:

1 - Agrupar registros da biblioteca por jogo
2 - Somar o tempo total jogado
3 - Contar quantos usuários jogaram cada jogo
4 - Calcular a média de minutos jogados por usuário
5 - Ordenar os jogos com maior engajamento médio
6 - Buscar informações do jogo na coleção de jogos
"""

from ..database import db


def engajamento_medio_jogos(limit: int = 5):

    """
    Retorna os jogos com maior tempo médio de gameplay por usuário.

    Parâmetros
    ----------
    limit : int
        Quantidade máxima de jogos retornados no ranking.

    Retorno
    -------
    list
        Lista contendo jogos com maior engajamento médio.
    """

    pipeline = [



        # -------------------------------------------------
        # ETAPA 1 — AGRUPAR REGISTROS POR JOGO
        # -------------------------------------------------
        #
        # Cada documento da coleção "biblioteca" representa
        # um jogo presente na biblioteca de um usuário,
        # juntamente com o tempo que ele jogou.
        #
        # Agrupamos por game_id para calcular estatísticas
        # relacionadas ao tempo de gameplay.
        #
        {
            "$group": {
                "_id": "$game_id",

                # soma total de minutos jogados
                "total_minutos": {
                    "$sum": "$minutos_jogados"
                },

                # número de jogadores
                "total_jogadores": {
                    "$sum": 1
                }
            }
        },


        # -------------------------------------------------
        # ETAPA 2 — CALCULAR MÉDIA DE TEMPO JOGADO
        # -------------------------------------------------
        #
        # Calcula quantos minutos, em média,
        # cada jogador passou naquele jogo.
        #
        {
            "$addFields": {
                "media_minutos_por_jogador": {
                    "$divide": [
                        "$total_minutos",
                        "$total_jogadores"
                    ]
                }
            }
        },



        # -------------------------------------------------
        # ETAPA 3 — ORDENAR PELO MAIOR ENGAJAMENTO
        # -------------------------------------------------
        #
        # Jogos com maior média de gameplay aparecem primeiro.
        #
        {
            "$sort": {
                "media_minutos_por_jogador": -1
            }
        },



        # -------------------------------------------------
        # ETAPA 4 — LIMITAR RESULTADO
        # -------------------------------------------------
        {
            "$limit": limit
        },



        # -------------------------------------------------
        # ETAPA 5 — BUSCAR INFORMAÇÕES DO JOGO
        # -------------------------------------------------
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
        {
            "$project": {

                "_id": 0,

                "game_id": "$game._id",

                "titulo": "$game.titulo",

                "media_minutos_por_jogador": {
                    "$round": ["$media_minutos_por_jogador", 2]
                },

                "total_jogadores": 1
            }
        }

    ]

    resultado = db["biblioteca"].aggregate(pipeline)

    return list(resultado)