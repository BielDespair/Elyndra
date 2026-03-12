"""
Buscar jogos pertencentes a uma categoria específica
e retornar informações organizadas para visualização
na API ou na interface Streamlit.

Essa abordagem utiliza Aggregation Pipeline do MongoDB
em vez de uma simples consulta (find), pois permite:

- Filtrar dados
- Transformar resultados
- Projetar apenas os campos necessários
- Ordenar os dados retornados
"""

from pymongo.database import Database



# FUNÇÃO PRINCIPAL



def buscar_games_por_categoria(db: Database, categoria: str):
    """
    Executa uma agregação na coleção 'games'
    para buscar todos os jogos pertencentes
    a uma determinada categoria.

    Parâmetros
    ----------
    db : Database
        Conexão ativa com o banco MongoDB.

    categoria : str
        Categoria de jogo utilizada como filtro.

    Retorno
    -------
    list
        Lista contendo os jogos da categoria informada.
    """

   



    # PIPELINE DE AGREGAÇÃO

    pipeline = [

        # -------------------------------------------------
        #FILTRAGEM DOS JOGOS POR CATEGORIA
        # -------------------------------------------------
        #
        # Utilizamos o operador $match para selecionar
        # apenas os jogos que pertencem à categoria
        # informada pelo usuário.
        #
        # Essa etapa funciona de forma semelhante
        # ao comando WHERE no SQL.
        #
        {
            "$match": {
                "categoria": categoria
            }
        },





        # -------------------------------------------------
        #PROJEÇÃO DOS CAMPOS RELEVANTES
        # -------------------------------------------------
        #
        # O operador $project permite definir quais
        # campos devem aparecer no resultado final.
        #
        # Isso evita retornar dados desnecessários
        # e torna a resposta da API mais eficiente.
        #
        {
            "$project": {

                # ocultar o id padrão se desejado
                "_id": 0,

                # campos que queremos retornar
                "game_id": "$_id",
                "nome": 1,
                "categoria": 1,
                "plataforma": 1,
                "ano_lancamento": 1
            }
        },




        # -------------------------------------------------
        #ORDENAÇÃO DOS RESULTADOS
        # -------------------------------------------------
        #
        # Ordenamos os jogos alfabeticamente pelo nome.
        # Isso melhora a experiência na interface
        # e torna os resultados mais organizados.
        #
        {
            "$sort": {
                "nome": 1
            }
        }

    ]



    # =====================================================
    # EXECUÇÃO DO PIPELINE
    # =====================================================

    result = db["games"].aggregate(pipeline)

    # convertendo cursor do MongoDB em lista Python
    return list(result)