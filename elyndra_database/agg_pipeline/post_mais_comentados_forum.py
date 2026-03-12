"""
Este módulo implementa um Aggregation Pipeline responsável
por identificar quais posts do fórum possuem maior número
de comentários.

Esse tipo de análise é importante para identificar discussões
mais populares dentro da comunidade.

Objetivos da análise:

1 - Relacionar posts com seus comentários
2 - Contar quantos comentários cada post possui
3 - Ordenar posts mais comentados
4 - Buscar informações do post e do usuário
"""

from ..database import db


def posts_mais_comentados(limit: int = 5):

    """
    Retorna os posts do fórum com maior número de comentários.

    Parâmetros
    ----------
    limit : int
        Quantidade máxima de posts retornados.

    Retorno
    -------
    list
        Lista contendo os posts mais comentados.
    """

    pipeline = [

        # -------------------------------------------------
        # ETAPA 1 — RELACIONAR POSTS COM COMENTÁRIOS
        # -------------------------------------------------
        #
        # Utilizamos $lookup para buscar todos os comentários
        # associados a cada post do fórum.
        #
        {
            "$lookup": {
                "from": "comentarios_forum",
                "localField": "_id",
                "foreignField": "post_id",
                "as": "comentarios"
            }
        },

        # -------------------------------------------------
        # ETAPA 2 — CONTAR QUANTIDADE DE COMENTÁRIOS
        # -------------------------------------------------
        #
        # O operador $size calcula quantos comentários
        # existem dentro do array "comentarios".
        #
        {
            "$addFields": {
                "total_comentarios": {
                    "$size": "$comentarios"
                }
            }
        },

        # -------------------------------------------------
        # ETAPA 3 — ORDENAR POSTS MAIS COMENTADOS
        # -------------------------------------------------
        #
        {
            "$sort": {
                "total_comentarios": -1
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
        # ETAPA 5 — BUSCAR INFORMAÇÕES DO USUÁRIO
        # -------------------------------------------------
        #
        # Busca os dados do autor do post.
        #
        {
            "$lookup": {
                "from": "usuarios",
                "localField": "usuario_id",
                "foreignField": "_id",
                "as": "usuario"
            }
        },

        {
            "$unwind": "$usuario"
        },

        # -------------------------------------------------
        # ETAPA 6 — FORMATAR RESULTADO FINAL
        # -------------------------------------------------
        #
        {
            "$project": {

                "_id": 0,

                "post_id": "$_id",

                "titulo_post": "$titulo",

                "autor": "$usuario.nome",

                "total_comentarios": 1
            }
        }

    ]

    resultado = db["forum"].aggregate(pipeline)

    return list(resultado)