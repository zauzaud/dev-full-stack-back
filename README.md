# Colecao de Games API

API REST para gerenciar sua colecao pessoal de jogos. Catalogue os games que voce jogou, de notas, registre horas jogadas e acompanhe seu progresso!

## Sobre o Projeto

Este projeto e o **back-end** de um MVP desenvolvido para a disciplina de Desenvolvimento Full Stack Basico. A API permite:

- Cadastrar jogos com informacoes detalhadas (titulo, descricao, nota, horas jogadas)
- Organizar jogos por **genero** (RPG, FPS, Aventura, etc.)
- Associar jogos a multiplas **plataformas** (PC, PS5, Xbox, Switch, etc.)
- Acompanhar o **status** de cada jogo (backlog, jogando, zerado, abandonado)
- Consultar e filtrar sua colecao de diversas formas

### Tecnologias Utilizadas

- **Python 3** - Linguagem principal
- **Flask** - Framework web
- **Flask-OpenAPI3** - Documentacao Swagger automatica
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados relacional
- **Flask-CORS** - Suporte a requisicoes cross-origin

## Estrutura do Banco de Dados

O sistema utiliza 3 tabelas principais com relacionamentos:

```
+-------------+       +------------------+       +------------+
|   genres    |       |  game_platforms  |       | platforms  |
+-------------+       +------------------+       +------------+
| id          |       | game_id (FK)     |       | id         |
| name        |       | platform_id (FK) |       | name       |
| description |       +------------------+       | manufacturer|
+-------------+              N:N                 +------------+
      |                       |
      | 1:N                   |
      v                       v
+--------------------------------------------------+
|                     games                         |
+--------------------------------------------------+
| id, title, description, release_date, rating     |
| hours_played, status, cover_url, genre_id (FK)   |
+--------------------------------------------------+
```

## Instalacao

### Pre-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositorio**

```bash
git clone https://github.com/seu-usuario/dev-full-stack-back.git
cd dev-full-stack-back
```

2. **Crie um ambiente virtual** (recomendado)

```bash
python -m venv venv
```

3. **Ative o ambiente virtual**

No Windows:

```bash
venv\Scripts\activate
```

No Linux/Mac:

```bash
source venv/bin/activate
```

4. **Instale as dependencias**

```bash
pip install -r requirements.txt
```

5. **Execute a aplicacao**

```bash
python app.py
```

A API estara disponivel em: `http://localhost:5000`

## Documentacao da API (Swagger)

Apos iniciar a aplicacao, acesse a documentacao interativa:

- **Swagger UI**: http://localhost:5000/openapi/swagger

### Formato das Respostas

As rotas de listagem retornam objetos com arrays:

- `GET /games` retorna: `{"games": [...]}`
- `GET /platforms` retorna: `{"platforms": [...]}`
- `GET /genres` retorna: `{"genres": [...]}`

### Rotas Disponiveis

#### Games

| Metodo   | Rota          | Descricao                                    |
| -------- | ------------- | -------------------------------------------- |
| `POST`   | `/games`      | Cadastra um novo jogo                        |
| `GET`    | `/games`      | Lista todos os jogos (com filtros opcionais) |
| `GET`    | `/games/{id}` | Busca um jogo pelo ID                        |
| `PATCH`  | `/games/{id}` | Atualiza parcialmente um jogo existente      |
| `DELETE` | `/games/{id}` | Remove um jogo da colecao                    |

> **Nota sobre PATCH vs PUT:** Utilizamos PATCH ao inves de PUT pois a atualizacao
> e parcial - apenas os campos enviados na requisicao sao modificados, os demais
> permanecem inalterados. PUT exigiria enviar todos os campos do recurso, o que hoje em dia nao e uma pratica comum em APIs REST modernas.

#### Platforms

| Metodo | Rota         | Descricao                    |
| ------ | ------------ | ---------------------------- |
| `GET`  | `/platforms` | Lista todas as plataformas   |
| `POST` | `/platforms` | Cadastra uma nova plataforma |

#### Genres

| Metodo | Rota      | Descricao               |
| ------ | --------- | ----------------------- |
| `GET`  | `/genres` | Lista todos os generos  |
| `POST` | `/genres` | Cadastra um novo genero |

### Exemplos de Requisicoes - Caso queira utilizar o curl

#### Cadastrar uma Plataforma

```bash
curl -X POST http://localhost:5000/platforms \
  -H "Content-Type: application/json" \
  -d '{"name": "PlayStation 5", "manufacturer": "Sony"}'
```

#### Cadastrar um Genero

```bash
curl -X POST http://localhost:5000/genres \
  -H "Content-Type: application/json" \
  -d '{"name": "RPG", "description": "Role-Playing Game"}'
```

#### Cadastrar um Jogo

```bash
curl -X POST http://localhost:5000/games \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Witcher 3: Wild Hunt",
    "description": "Um RPG de mundo aberto aclamado pela critica",
    "release_date": "2015-05-19",
    "rating": 9.5,
    "hours_played": 150,
    "status": "completed",
    "genre_id": 1,
    "platform_ids": [1]
  }'
```

#### Listar Jogos com Filtro

```bash
# Listar apenas jogos com status "completed"
curl http://localhost:5000/games?status=completed

# Listar jogos de um genero especifico
curl http://localhost:5000/games?genre_id=1
```

### Status de Jogos

Os jogos podem ter os seguintes status:

| Status      | Descricao           |
| ----------- | ------------------- |
| `backlog`   | Na lista para jogar |
| `playing`   | Jogando atualmente  |
| `completed` | Zerado/Finalizado   |
| `abandoned` | Abandonado          |

## Estrutura do Projeto

```
dev-full-stack-back/
├── app.py              # Aplicacao principal e rotas da API
├── models.py           # Modelos do banco de dados (SQLAlchemy)
├── schemas.py          # Schemas de validacao (Pydantic)
├── database.py         # Configuracao do banco de dados
├── requirements.txt    # Dependencias do projeto
├── README.md           # Este arquivo
└── database/           # Pasta do banco SQLite (criada automaticamente)
    └── games_collection.db
```

## Autor

Desenvolvido com <3 para o MVP da disciplina de Desenvolvimento Full Stack Basico - PUC-Rio.

## Licenca

Este projeto esta sob a licenca MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
