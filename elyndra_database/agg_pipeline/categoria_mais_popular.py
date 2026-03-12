"""
Este módulo implementa um Aggregation Pipeline responsável
por identificar quais categorias de jogos são mais populares
entre os usuários da plataforma.

A análise considera:

- quantidade de jogos por categoria
- popularidade das categorias dentro da plataforma
"""

from ..database import db


def categorias_mais_populares(limit: int = 5):

    """
    Retorna as categorias de jogos mais populares.

    Parâmetros
    ----------
    limit : int
        Quantidade máxima de categorias retornadas.

    Retorno
    -------
    list
        Lista contendo as categorias mais populares.
    """

    pipeline = [



        # -------------------------------------------------
        # ETAPA 1 — DESMEMBRAR ARRAY DE CATEGORIAS
        # -------------------------------------------------
        #
        # Muitos jogos podem possuir múltiplas categorias
        # (ex: RPG, Ação, Aventura).
        #
        # O operador $unwind transforma cada categoria
        # em um documento separado para permitir contagem.
        #
        {
            "$unwind": "$categorias"
        },



        # -------------------------------------------------
        # ETAPA 2 — AGRUPAR POR CATEGORIA
        # -------------------------------------------------
        #
        # Aqui contamos quantos jogos existem
        # em cada categoria.
        #
        {
            "$group": {

                "_id": "$categorias",

                "total_jogos": {
                    "$sum": 1
                }

            }
        },



        # -------------------------------------------------
        # ETAPA 3 — ORDENAR CATEGORIAS
        # -------------------------------------------------
        #
        # Ordenamos da categoria com mais jogos
        # para a com menos jogos.
        #
        {
            "$sort": {
                "total_jogos": -1
            }
        },




        # -------------------------------------------------
        # ETAPA 4 — LIMITAR RESULTADOS
        # -------------------------------------------------
        #
        # Retorna apenas as categorias mais populares.
        #
        {
            "$limit": limit
        },




        # -------------------------------------------------
        # ETAPA 5 — FORMATAR RESULTADO FINAL
        # -------------------------------------------------
        #
        {
            "$project": {

                "_id": 0,

                "categoria": "$_id",

                "total_jogos": 1

            }
        }

    ]

    resultado = db["games"].aggregate(pipeline)

    return list(resultado)