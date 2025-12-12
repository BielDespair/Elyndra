from elyndra_database.bootstrap import *
from elyndra_database.database import db

def main():    
    seed_usuarios(db)
    seed_catalogo(db)

if __name__ == "__main__":
    main()
