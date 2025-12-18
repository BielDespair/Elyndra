from elyndra_database.bootstrap import *
from elyndra_database.database import db, client


DROP_DATABASE = True


def main():
    if DROP_DATABASE:
        client.drop_database("elyndra")
        
        
    seed_usuarios(db)
    seed_games(db)
    seed_biblioteca(db)
    seed_reviews(db)
    seed_forum(db)
    

if __name__ == "__main__":
    main()