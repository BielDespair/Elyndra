"""
Este módulo implementa um Aggregation Pipeline responsável
por analisar como os jogos da plataforma estão distribuídos
entre diferentes categorias.

Essa análise é importante para:

- compreender a estrutura do catálogo
- gerar gráficos para dashboards administrativos
- identificar categorias mais populares
- apoiar decisões estratégicas da plataforma

Coleção utilizada:

Resultado esperado:

Lista contendo cada categoria existente e o número de jogos
presentes em cada uma delas.
"""


from ..database import db


def distribuicao_jogos_por_categoria():
    
    """
    Retorna a quantidade de jogos existentes em cada categoria.

    Retorno
    -------
    list
        Lista contendo categorias e número total de jogos.
    """


    pipeline = [

        # ----------------------------------------------------
        # ETAPA 1 — AGRUPAR JOGOS POR CATEGORIA
        # ----------------------------------------------------
        #
        # Utilizamos o operador $group para agrupar
        # todos os jogos existentes na coleção "games"
        # com base no campo "categoria".
        #
        # Para cada categoria calculamos:
        #
        # total_jogos → quantidade de jogos naquela categoria
        #
        {
            "$group": {
                "_id": "$categoria",

                "total_jogos": {
                    "$sum": 1
                }
            }
        },



        # ----------------------------------------------------
        # ETAPA 2 — ORDENAR RESULTADOS
        # ----------------------------------------------------
        #
        # Ordenamos as categorias da que possui
        # mais jogos para a que possui menos.
        #
        {
            "$sort": {
                "total_jogos": -1
            }
        },



        # ----------------------------------------------------
        # ETAPA 3 — FORMATAR RESULTADO FINAL
        # ----------------------------------------------------
        #
        # Utilizamos $project para reorganizar
        # a estrutura dos dados retornados.
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