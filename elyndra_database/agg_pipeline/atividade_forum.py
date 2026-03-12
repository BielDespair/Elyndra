"""
Este módulo implementa um Aggregation Pipeline responsável
por identificar os posts mais populares do fórum da plataforma.

A análise considera:

- número de comentários
- interação dos usuários

Objetivos:

1 - Agrupar comentários por post
2 - Contar quantos comentários cada post possui
3 - Ordenar os posts mais comentados
4 - Buscar informações do post
5 - Buscar informações do autor do post

Coleções utilizadas:

comentarios_forum → comentários feitos pelos usuários
forum → posts criados no fórum
usuarios → autores dos posts
"""

from ..database import db


def posts_mais_populares(limit: int = 5):

    """
    Retorna os posts mais populares do fórum com base
    na quantidade de comentários.

    Parâmetros
    ----------
    limit : int
        Número máximo de posts retornados.

    Retorno
    -------
    list
        Lista contendo posts mais comentados da plataforma.
    """





    pipeline = [

        # -------------------------------------------------
        # ETAPA 1 — AGRUPAR COMENTÁRIOS POR POST
        # -------------------------------------------------
        #
        # Cada documento da coleção comentarios_forum
        # representa um comentário feito em um post.
        #
        # Aqui agrupamos por post_id para descobrir
        # quantos comentários cada post possui.
        #
        {
            "$group": {
                "_id": "$post_id",

                "total_comentarios": {
                    "$sum": 1
                }
            }
        },



        # -------------------------------------------------
        # ETAPA 2 — ORDENAR PELOS POSTS MAIS COMENTADOS
        # -------------------------------------------------
        #
        # Ordena os posts com maior quantidade
        # de comentários primeiro.
        #
        {
            "$sort": {
                "total_comentarios": -1
            }
        },



        # -------------------------------------------------
        # ETAPA 3 — LIMITAR RESULTADOS
        # -------------------------------------------------
        #
        # Define quantos posts aparecerão no ranking.
        #
        {
            "$limit": limit
        },



        # -------------------------------------------------
        # ETAPA 4 — BUSCAR INFORMAÇÕES DO POST
        # -------------------------------------------------
        #
        # Realiza junção com a coleção de posts do fórum.
        #
        {
            "$lookup": {
                "from": "forum",
                "localField": "_id",
                "foreignField": "_id",
                "as": "post"
            }
        },

        {
            "$unwind": "$post"
        },



        # -------------------------------------------------
        # ETAPA 5 — BUSCAR INFORMAÇÕES DO AUTOR
        # -------------------------------------------------
        #
        # Busca dados do usuário que criou o post.
        #
        {
            "$lookup": {
                "from": "usuarios",
                "localField": "post.usuario_id",
                "foreignField": "_id",
                "as": "autor"
            }
        },

        {
            "$unwind": "$autor"
        },



        # -------------------------------------------------
        # ETAPA 6 — FORMATAR RESULTADO FINAL
        # -------------------------------------------------
        #
        # Define os campos que serão exibidos.
        #
        {
            "$project": {

                "_id": 0,

                "post_id": "$post._id",

                "titulo_post": "$post.titulo",

                "autor": "$autor.nome",

                "total_comentarios": 1
            }
        }

    ]

    resultado = db["comentarios_forum"].aggregate(pipeline)

    return list(resultado)
