"""
Este módulo implementa um Aggregation Pipeline responsável
por identificar quais usuários possuem maior participação
no fórum da plataforma.

A análise considera:

- quantidade de posts criados
- quantidade de comentários feitos

Objetivos:

1 - Agrupar atividades por usuário
2 - Contabilizar número de posts
3 - Contabilizar número de comentários
4 - Calcular total de interações
5 - Ordenar usuários mais ativos
6 - Buscar informações do usuário
"""

from ..database import db


def ranking_usuarios_forum(limit: int = 5):

    """
    Retorna os usuários mais ativos no fórum.

    Parâmetros
    ----------
    limit : int
        Quantidade máxima de usuários retornados.

    Retorno
    -------
    list
        Lista contendo ranking de participação no fórum.
    """

    pipeline = [

        # -------------------------------------------------
        # ETAPA 1 — AGRUPAR POSTS POR USUÁRIO
        # -------------------------------------------------
        #
        # Cada documento da coleção "forum"
        # representa um post criado por um usuário.
        #
        {
            "$group": {
                "_id": "$usuario_id",

                "total_posts": {
                    "$sum": 1
                }
            }
        },

        # -------------------------------------------------
        # ETAPA 2 — BUSCAR COMENTÁRIOS DO USUÁRIO
        # -------------------------------------------------
        #
        # Utilizamos $lookup para contar quantos
        # comentários cada usuário fez no fórum.
        #
        {
            "$lookup": {
                "from": "comentarios_forum",
                "localField": "_id",
                "foreignField": "usuario_id",
                "as": "comentarios"
            }
        },

        # -------------------------------------------------
        # ETAPA 3 — CONTAR COMENTÁRIOS
        # -------------------------------------------------
        #
        # Calcula quantos comentários o usuário possui.
        #
        {
            "$addFields": {
                "total_comentarios": {
                    "$size": "$comentarios"
                }
            }
        },

        # -------------------------------------------------
        # ETAPA 4 — CALCULAR TOTAL DE INTERAÇÕES
        # -------------------------------------------------
        #
        # Soma posts + comentários.
        #
        {
            "$addFields": {
                "total_interacoes": {
                    "$add": [
                        "$total_posts",
                        "$total_comentarios"
                    ]
                }
            }
        },

        # -------------------------------------------------
        # ETAPA 5 — ORDENAR USUÁRIOS MAIS ATIVOS
        # -------------------------------------------------
        #
        {
            "$sort": {
                "total_interacoes": -1
            }
        },

        # -------------------------------------------------
        # ETAPA 6 — LIMITAR RESULTADO
        # -------------------------------------------------
        #
        {
            "$limit": limit
        },

        # -------------------------------------------------
        # ETAPA 7 — BUSCAR DADOS DO USUÁRIO
        # -------------------------------------------------
        #
        {
            "$lookup": {
                "from": "usuarios",
                "localField": "_id",
                "foreignField": "_id",
                "as": "usuario"
            }
        },

        {
            "$unwind": "$usuario"
        },

        # -------------------------------------------------
        # ETAPA 8 — FORMATAR RESULTADO FINAL
        # -------------------------------------------------
        #
        {
            "$project": {

                "_id": 0,

                "usuario_id": "$usuario._id",

                "nome_usuario": "$usuario.nome",

                "total_posts": 1,

                "total_comentarios": 1,

                "total_interacoes": 1
            }
        }

    ]

    resultado = db["forum"].aggregate(pipeline)

    return list(resultado)