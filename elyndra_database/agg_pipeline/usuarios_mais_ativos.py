"""
Este módulo contém um pipeline de agregação responsável
por identificar os usuários mais ativos da plataforma.

Objetivos da análise:

1 - Calcular o tempo total jogado por cada usuário
2 - Contabilizar quantos jogos diferentes cada usuário possui
3 - Ordenar os usuários pelos mais ativos
4 - Buscar informações do usuário na coleção de usuários

Esse tipo de análise pode ser utilizado para:

- rankings da plataforma
- gamificação
- dashboards administrativos
- análise de engajamento de usuários
"""

from ..database import db


def ranking_usuarios_ativos(limit: int = 5):

    """
    Retorna um ranking dos usuários mais ativos da plataforma.

    Parâmetros
    ----------
    limit : int
        Número máximo de usuários que devem aparecer no ranking.

    Retorno
    -------
    list
        Lista contendo os usuários mais ativos e suas estatísticas.
    """

    pipeline = [

        # -------------------------------------------------------
        # ETAPA 1 — AGRUPAR DADOS POR USUÁRIO
        # -------------------------------------------------------
        #
        # Cada documento da coleção "biblioteca" representa
        # um registro de jogo de um usuário.
        #
        # Aqui agrupamos esses registros pelo campo "usuario_id"
        # para consolidar os dados de cada usuário.
        #
        {
            "$group": {
                "_id": "$usuario_id",

                # Soma de todos os minutos jogados
                "total_minutos": {
                    "$sum": "$minutos_jogados"
                },

                # Quantidade de jogos diferentes
                "total_jogos": {
                    "$sum": 1
                }
            }
        },






        # ETAPA 2 — ORDENAÇÃO DOS USUÁRIOS
       


        #
        # Ordenamos os usuários pelo maior tempo jogado.
        #
        {
            "$sort": {
                "total_minutos": -1
            }
        },



       

        # ETAPA 3 — LIMITAR RESULTADOS
        # -------------------------------------------------------
        #
        # Define quantos usuários aparecerão no ranking.
        #
        {
            "$limit": limit
        },



      
        # ETAPA 4 — BUSCAR INFORMAÇÕES DO USUÁRIO
    


        #
        # Utilizamos $lookup para buscar dados adicionais
        # na coleção "usuarios".
        #
        {
            "$lookup": {
                "from": "usuarios",
                "localField": "_id",
                "foreignField": "_id",
                "as": "usuario"
            }
        },



        # ETAPA 5 — TRANSFORMAR ARRAY EM OBJETO
       


        #
        # O resultado do lookup vem como array.
        # Utilizamos $unwind para simplificar.
        #
        {
            "$unwind": "$usuario"
        },





        # ETAPA 6 — FORMATAR RESULTADO FINAL
      

        #
        # Define quais campos aparecerão no ranking.
        #
        {
            "$project": {

                "_id": 0,

                "usuario_id": "$usuario._id",

                "nome_usuario": "$usuario.nome",

                "total_minutos": 1,

                "total_jogos": 1
            }
        }

    ]

    resultado = db["biblioteca"].aggregate(pipeline)

    return list(resultado)



