"""
Este módulo contém uma função responsável por calcular quais jogos
possuem maior tempo total de gameplay dentro da plataforma Elyndra.

Objetivos da análise:

1. Agrupar registros de gameplay por jogo
2. Somar o tempo total jogado por todos os usuários
3. Contabilizar quantos jogadores distintos jogaram cada jogo
4. Ordenar os jogos do mais jogado para o menos jogado
5. Buscar informações adicionais do jogo na coleção de jogos
6. Retornar um resultado estruturado para uso na API ou interface

Resultado esperado:

Lista contendo os jogos mais jogados da plataforma.
"""

# Importa a conexão com o banco de dados
from ..database import db


def jogos_mais_jogados(limit: int = 5):

    """
    Retorna os jogos mais jogados da plataforma Elyndra.

    Parâmetros
    ----------
    limit : int
        Quantidade máxima de jogos que devem ser retornados.
        Por padrão retorna os 5 jogos mais jogados.

    Retorno
    -------
    list
        Lista contendo informações analíticas sobre os jogos
        com maior tempo total de gameplay.
    """

    


    # DEFINIÇÃO DO AGGREGATION PIPELINE



    pipeline = [

        # --------------------------------------------------------
        # ETAPA 1 — AGRUPAMENTO DOS DADOS POR JOGO
        # --------------------------------------------------------
        #
        # Nesta etapa utilizamos o operador $group para consolidar
        # os registros de gameplay existentes na coleção "biblioteca".
        #
        # Cada documento da coleção representa um registro de jogo
        # de um usuário específico.
        #
        # O agrupamento é realizado utilizando o campo "game_id".
        #
        # Para cada jogo calculamos:
        #
        # total_minutos → soma total de minutos jogados
        # jogadores → quantidade de usuários que jogaram o jogo
        #
        {
            "$group": {
                "_id": "$game_id",

                # Soma de todos os minutos jogados
                "total_minutos": {
                    "$sum": "$minutos_jogados"
                },

                # Contagem de registros de jogadores
                "jogadores": {
                    "$sum": 1
                }
            }
        },



       
        # ETAPA 2 — ORDENAÇÃO DOS RESULTADOS
    


        #
        # Após calcular o total de minutos jogados por jogo,
        # ordenamos os resultados em ordem decrescente.
        #
        # Isso garante que os jogos mais jogados apareçam primeiro.
        #
        {
            "$sort": {
                "total_minutos": -1
            }
        },



       
        # ETAPA 3 — LIMITAÇÃO DO RESULTADO
      


        #
        # Utilizamos o operador $limit para restringir
        # a quantidade de resultados retornados.
        #
        # Isso é útil para gerar rankings como:
        #
        # Top 5 jogos mais jogados
        # Top 10 jogos mais jogados
        #
        {
            "$limit": limit
        },





        
        # ETAPA 4 — JUNÇÃO COM A COLEÇÃO DE JOGOS



        #
        # A coleção "biblioteca" contém apenas o identificador
        # do jogo (game_id).
        #
        # Para obter o título e outras informações do jogo,
        # realizamos uma junção com a coleção "games"
        # utilizando o operador $lookup.
        #
        # Esse operador funciona de forma semelhante
        # a um JOIN em bancos de dados relacionais.
        #
        {
            "$lookup": {
                "from": "games",
                "localField": "_id",
                "foreignField": "_id",
                "as": "game"
            }
        },





        # ETAPA 5 — DESNORMALIZAÇÃO DO RESULTADO
   


        #
        # O operador $lookup retorna os dados em formato de array.
        #
        # Como cada jogo possui apenas um registro correspondente,
        # utilizamos $unwind para transformar o array em um objeto
        # simples dentro do documento.
        #
        {
            "$unwind": "$game"
        },



     
        # ETAPA 6 — DEFINIÇÃO DO FORMATO FINAL DOS DADOS
     

        #
        # O operador $project permite definir quais campos
        # devem ser retornados no resultado final da agregação.
        #
        # Também utilizamos essa etapa para reorganizar
        # a estrutura do documento retornado.
        #
        {
            "$project": {

                # Remove o campo _id original do resultado
                "_id": 0,

                # Identificador do jogo
                "game_id": "$game._id",

                # Título do jogo
                "titulo": "$game.titulo",

                # Estatísticas calculadas
                "total_minutos": 1,
                "jogadores": 1
            }
        }

    ]





   
    # EXECUÇÃO DO PIPELINE
   

   

    resultado = db["biblioteca"].aggregate(pipeline)

    # Converte o cursor retornado pelo MongoDB em lista Python
    return list(resultado)