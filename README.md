## Elyndra — Plataforma de Jogos
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)

Elyndra é uma plataforma digital baseada no funcionamento da [Steam](https://store.steampowered.com/), permitindo visualização, download e gerenciamento de jogos.  
O usuário cria uma conta, acessa um catálogo de títulos (gratuitos ou pagos) e adiciona os jogos adquiridos à sua biblioteca pessoal.

### Funcionalidades
- Perfil com conquistas, estatísticas e histórico de jogo.  
- Biblioteca com todos os títulos adquiridos e disponíveis para download.  
- Lista de amigos e comunicação básica entre usuários.  
- Recomendações de jogos de acordo com o perfil de consumo.
- Avaliações publicadas por perfis de usuários em cada jogo.  

### Loja
- Catálogo completo para compra.
- Disponibilização do download dos títulos.
- Página individual de cada jogo com descrição, requisitos, avaliações e sugestões de títulos relacionados.

### Estrutura
- **Página Principal:** perfil, conquistas, estatísticas, amigos e biblioteca.  
- **Página da Loja:** catálogo, detalhes dos jogos, avaliações e acesso ao fórum de cada título.  
- **Comunidade:** fóruns, discussões e troca de informações entre usuários.


## Organização do Projeto

O projeto é dividido em dois módulos principais, com responsabilidades bem definidas.

### `elyndra_app` - API

Este módulo contém a aplicação web construída com **FastAPI**.  Representa a **camada de aplicação**

Responsabilidades:
- Expor a API REST do sistema.
- Definir rotas, validações e contratos de dados.
- Aplicar regras de negócio.
- Orquestrar o acesso ao banco de dados.

---

### `elyndra_database` - Banco de Dados

Este módulo concentra tudo relacionado ao **MongoDB** e suas operações no banco de dados.

Responsabilidades:
- Scripts de inicialização (bootstrap/seed) do banco.
- Operações diretas de banco, fora do contexto HTTP.



---

## Estrutura de Diretórios

```text
.
├── bootstrap.py
│
├── elyndra_app/
│   ├── main.py
│   └── models/
│   
├── elyndra_database/
│   ├── bootstrap/
│   │   ├── seed_usuarios.py
│   │   ├── seed_games.py
│   │   ├── seed_biblioteca.py
│   │   ├── seed_reviews.py
│   │   ├── seed_forum.py
│   │   └── seeds/
│   │       ├── users.json
│   │       ├── games.json
│   │       ├── reviews.json
│   │       └── forum.json
│
└── README.md
```

## Como executar
```bash
git clone https://github.com/BielDespair/Elyndra.git
cd Elyndra
pip install -r requirements.txt
```

Crie um arquivo .env na raiz do projeto, preenchendo as variáveis de ambiente
```text
DB_USER="<SEU_USUARIO>"
DB_PASSWORD="<SUA_SENHA>"
```

### Inicialização do Banco de Dados
Rode o script bootstrap.py para inicializar o banco com alguns dados iniciais.

> [!CAUTION]
> **Atenção à variável `DROP_DATABASE` no arquivo `bootstrap.py`:**
> - Se definida como `True`: O script irá **DELETAR** todas as coleções existentes no banco `elyndra`.

```bash
python bootstrap.py
```

### Executar o servidor uvicorn
```
uvicorn elyndra_app.main:app --reload
```

