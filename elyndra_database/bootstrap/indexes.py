def create_indexes(db):

    #Usuário

    db["usuarios"].create_index("email", unique=True)

    #Jogos

    db["games"].create_index("titulo")

    #Biblioteca

    db["biblioteca"].create_index(
        [("user_id", 1), ("game_id", 1)],
        unique=True
    )

    #Reviews

    db["reviews"].create_index(
        [("user_id", 1), ("game_id", 1)],
        unique=True
    )
    db["reviews"].create_index("game_id")

    #Fórum
    
    db["forum"].create_index("game_id")
    db["forum"].create_index("created_at")

    print("Indexes criados com sucesso")
