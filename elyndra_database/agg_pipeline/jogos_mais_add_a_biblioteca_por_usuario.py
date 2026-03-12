"""
Este módulo implementa um Aggregation Pipeline responsável
por identificar quais jogos estão presentes na maior quantidade
de bibliotecas de usuários.

Diferente do pipeline de "jogos mais jogados", que analisa
tempo de gameplay, este pipeline mede a popularidade
dos jogos com base em quantos usuários possuem o jogo
em sua biblioteca.

Objetivos da análise:

1 - Contar quantas vezes cada jogo aparece na biblioteca
2 - Criar um ranking de popularidade
3 - Buscar informações do jogo na coleção de jogos
4 - Retornar os jogos mais presentes nas bibliotecas
"""

from ..database import db


def jogos_mais_populares_biblioteca(limit: int = 5):

    """
    Retorna os jogos que aparecem em mais bibliotecas de usuários.

    Parâmetros
    ----------
    limit : int
        Quantidade máxima de jogos no ranking.

    Retorno
    -------
    list
        Lista contendo os jogos mais presentes nas bibliotecas.
    """



    pipeline = [

        # -------------------------------------------------
        # ETAPA 1 — AGRUPAR REGISTROS POR JOGO
        # -------------------------------------------------
        #
        # Cada documento da coleção "biblioteca" representa
        # um jogo que pertence à biblioteca de um usuário.
        #
        # Agrupamos por game_id para descobrir quantos
        # usuários possuem aquele jogo.
        #
        {
            "$group": {
                "_id": "$game_id",

                # número de usuários que possuem o jogo
                "total_usuarios": {
                    "$sum": 1
                }
            }
        },




        # -------------------------------------------------
        # ETAPA 2 — ORDENAR PELOS JOGOS MAIS POPULARES
        # -------------------------------------------------
        #
        # Ordena os jogos pela maior quantidade
        # de bibliotecas.
        #
        {
            "$sort": {
                "total_usuarios": -1
            }
        },



        # -------------------------------------------------
        # ETAPA 3 — LIMITAR RESULTADOS
        # -------------------------------------------------
        #
        # Define quantos jogos aparecerão no ranking.
        #
        {
            "$limit": limit
        },




        # -------------------------------------------------
        # ETAPA 4 — BUSCAR INFORMAÇÕES DO JOGO
        # -------------------------------------------------
        #
        # Utilizamos $lookup para buscar o título do jogo
        # na coleção "games".
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
        # Define quais campos serão exibidos.
        #
        {
            "$project": {

                "_id": 0,

                "game_id": "$game._id",

                "titulo": "$game.titulo",

                "total_usuarios": 1
            }
        }

    ]

    resultado = db["biblioteca"].aggregate(pipeline)

    return list(resultado)