"""
Este módulo implementa um Aggregation Pipeline responsável
por identificar quais jogos geram maior número de discussões
no fórum da plataforma.

A análise considera:

- quantidade de posts relacionados a cada jogo
- atividade da comunidade em torno do jogo

Objetivos da análise:

1 - Agrupar posts do fórum por jogo
2 - Contar quantos posts existem para cada jogo
3 - Ordenar os jogos com mais discussões
4 - Buscar informações do jogo na coleção de jogos
"""

from ..database import db


def jogos_mais_discutidos_forum(limit: int = 5):

    """
    Retorna os jogos que possuem mais discussões no fórum.

    Parâmetros
    ----------
    limit : int
        Número máximo de jogos retornados.

    Retorno
    -------
    list
        Lista contendo os jogos mais discutidos no fórum.
    """



    pipeline = [

        # -------------------------------------------------
        # ETAPA 1 — AGRUPAR POSTS DO FÓRUM POR JOGO
        # -------------------------------------------------
        #
        # Cada documento da coleção "forum"
        # representa um post criado por um usuário.
        #
        # Agrupamos pelo campo game_id para identificar
        # quantas discussões existem para cada jogo.
        #
        {
            "$group": {
                "_id": "$game_id",

                "total_posts": {
                    "$sum": 1
                }
            }
        },

        # -------------------------------------------------
        # ETAPA 2 — ORDENAR PELOS JOGOS MAIS DISCUTIDOS
        # -------------------------------------------------
        #
        {
            "$sort": {
                "total_posts": -1
            }
        },

        # -------------------------------------------------
        # ETAPA 3 — LIMITAR RESULTADO
        # -------------------------------------------------
        #
        {
            "$limit": limit
        },

        # -------------------------------------------------
        # ETAPA 4 — BUSCAR INFORMAÇÕES DO JOGO
        # -------------------------------------------------
        #
        # Realiza junção com a coleção "games"
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

        {
            "$unwind": "$game"
        },

        # -------------------------------------------------
        # ETAPA 5 — FORMATAR RESULTADO FINAL
        # -------------------------------------------------
        #
        {
            "$project": {

                "_id": 0,

                "game_id": "$game._id",

                "titulo": "$game.titulo",

                "total_posts": 1
            }
        }

    ]

    resultado = db["forum"].aggregate(pipeline)

    return list(resultado)