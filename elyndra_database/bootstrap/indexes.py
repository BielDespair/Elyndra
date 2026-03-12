"""
Elyndra - Criação de Indexes no MongoDB

Os índices são utilizados para melhorar a performance
das consultas no banco de dados.

Sem índices, o MongoDB precisaria percorrer todos os
documentos da coleção para encontrar resultados
(full collection scan).

Com índices, o banco consegue localizar os documentos
de forma muito mais eficiente.
"""





def create_indexes(db):

    # -------------------------------------------------
    # COLEÇÃO: USUARIOS
    # -------------------------------------------------
    #
    # O e-mail de cada usuário deve ser único no sistema.
    #
    # Esse índice garante duas coisas:
    #
    # 1) Busca rápida por email (ex: login)
    # 2) Impede duplicidade de cadastro
    #
    db["usuarios"].create_index(
        "email",
        unique=True
    )




    # -------------------------------------------------
    # COLEÇÃO: GAMES
    # -------------------------------------------------
    #
    # Índice para busca de jogos por título.
    #
    # Esse índice melhora consultas como:
    #
    # buscar jogo pelo nome
    # filtros na interface
    #
    db["games"].create_index("titulo")




    # -------------------------------------------------
    # COLEÇÃO: BIBLIOTECA
    # -------------------------------------------------
    #
    # Essa coleção representa os jogos que cada usuário possui.
    #
    # O índice composto garante que:
    #
    # - um usuário não possa adicionar o mesmo jogo duas vezes
    #
    # Exemplo:
    #
    # user_id + game_id
    #
    # Cada combinação deve ser única.
    #
    db["biblioteca"].create_index(
        [("user_id", 1), ("game_id", 1)],
        unique=True
    )




    # -------------------------------------------------
    # COLEÇÃO: REVIEWS
    # -------------------------------------------------
    #
    # Cada usuário só pode avaliar um jogo uma única vez.
    #
    # O índice composto impede múltiplas avaliações
    # do mesmo usuário para o mesmo jogo.
    #
    db["reviews"].create_index(
        [("user_id", 1), ("game_id", 1)],
        unique=True
    )

    #
    # Índice adicional para consultas por jogo.
    #
    # Usado em operações como:
    #
    # - calcular média de avaliações
    # - buscar reviews de um jogo
    #
    db["reviews"].create_index("game_id")




    # -------------------------------------------------
    # COLEÇÃO: FORUM
    # -------------------------------------------------
    #
    # Índice para buscar discussões relacionadas
    # a um jogo específico.
    #
    db["forum"].create_index("game_id")

    #
    # Índice para ordenar discussões por data.
    #
    # Permite consultas como:
    #
    # - discussões mais recentes
    # - histórico do fórum
    #
    db["forum"].create_index("created_at")


    print("Indexes criados com sucesso")