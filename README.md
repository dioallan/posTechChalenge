# posTechChalenge
Repositorio TechChalengeFiap

API RESTful para gerenciamento, consulta e análise de livros, com scraping, autenticação JWT, estatísticas, integração com Prometheus, endpoints para Machine Learning e logging estruturado.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Instalação](#instalacao)
- [Configuração](#configuracao)
- [Endpoints Principais](#endpoints-principais)
    - [Endpoints Obrigatórios](#endpoints-obrigatorio)       
    - [Endpoints Adicionais](#endpoints-adicional)
- [Autenticação JWT](#autenticacao-jwt)
- [Scraping](#scraping)
- [Machine Learning](#machine-learning)
- [Logs](#logs)
- [Monitoramento](#monitoramento)

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Sobre o Projeto

Esta API permite:

Gerenciar e consultar um catálogo de livros.
Realizar scraping de dados de livros.
Autenticar usuários via JWT.
Expor métricas Prometheus.
Fornecer endpoints para análise estatística e Machine Learning.
Registrar logs estruturados em formato NDJSON.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Funcionalidades

CRUD de livros (via scraping e importação).
Busca por título, categoria e faixa de preço.
Estatísticas gerais e por categoria.
Endpoints para consumo e predição de modelos de Machine Learning.
Autenticação JWT.
Logging estruturado.
Swagger UI para documentação interativa.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Instalação

1. - Clone o repositório:

bash


```bash
git clone https://github.com/dioallan/posTechChalenge.git
cd seu-repo
Crie um ambiente virtual:

```
2. - Crie um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
Instale as dependências:
```
3. - Instale as dependências:

```bash

pip install -r requirements.txt

```

4. - Configure o banco de dados e variáveis de ambiente (ver seção Configuração).

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Configuração

1. - Ao Inicializar a aplicação é criado um Banco De Dados, para servir como backup do Dataframe, com origem do arquivo .csv gerado através do processo de Scraping.
  
   - Tabela usuario e livros:
     
```python
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<Usuario {self.nome}>"


class Livros(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    preco_sem_taxa = db.Column(db.Float, nullable=False)
    preco_com_taxa = db.Column(db.Float, nullable=False)
    disponibilidade = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    classificacao_em_estrelas = db.Column(db.Integer, nullable=False)
    url_imagem = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<Livros {self.titulo}>"

```

Acesse a documentação interativa:
http://localhost:5000/apidocs

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Endpoints Principais e Exemplos de chamadas com retorno:

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Autenticação JWT

![Desenho Usuário](images/rota_usuario.jpg)

POST /api/v1/auth/login — Login e obtenção de token JWT.

Exemplo de Entrada:
```json
{
    "username": "admin",
    "password": "1234"
}
```

Exemplo de Retorno:

```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NDg4MzYyNSwianRpIjoiM2JiMGNiM2MtNzI3OS00MmQ2LWJjMjQtMjNhNmQzYjNiMmU2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NTQ4ODM2MjUsImNzcmYiOiI0MGFjNmEyYi01ZTQxLTQ5OTctOGI2Ny1kZjI2NTg4NGQwNjYiLCJleHAiOjE3NTQ4ODQ1MjV9.hXL2o4l50giXRke0t0IjkY4ePjJdSETND9CjsUx_7L8",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NDg4MzYyNSwianRpIjoiMjQ3MTVhMDYtYzcyZS00MTQzLWI4ZTMtNTNhNTk2NWI2ZDA1IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiIxIiwibmJmIjoxNzU0ODgzNjI1LCJjc3JmIjoiNWJmNzIxMTEtZjhjMC00MWM0LWI3N2EtNDc1MTY0NDNjMmVlIiwiZXhwIjoxNzU3NDc1NjI1fQ.1y1izk0Xq6gjpyRptnd-_iG7di7lmDYuYH5h0eH6VgQ"
}
```

POST /api/v1/auth/refresh — Renovação do token de acesso.

Exemplo de Entrada:

```json
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NDgwMzI2OSwianRpIjoiMGZkMGY5YTQtOWZjYS00YmM5LWJjODgtMDRmNzQ5MWZjYjAyIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiIxIiwibmJmIjoxNzU0ODAzMjY5LCJjc3JmIjoiZjA5NDNlZDUtOGY2OS00OTI4LWJjNmItYTNmYTE4MDU4OWE2IiwiZXhwIjoxNzU3Mzk1MjY5fQ.TFnji2dem9OIveGRVGODCxGL0dnD8iYySwkof7Te8kQ
```
Exemplo de Retorno:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NDg4Mzg1OCwianRpIjoiMDEwN2ViNWYtYmVkYi00NjYwLWFjYjUtODY1ZDJlZTlkOTljIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NTQ4ODM4NTgsImNzcmYiOiIzNWY1OGVhNi0xYzQxLTQ1YzItOTEyYS0zNGFlNjY5NWNhN2IiLCJleHAiOjE3NTQ4ODQ3NTh9.pNqYSXrZS14bnEb-AJ6mWasQw13fklTXKmHONph300w"
}
```


POST /api/v1/auth/newuser — Criação de novo usuário (JWT).

Exemplo de Entrada:

```json
{
    "username": "admin6",
    "password": "12345"
}
```
Exemplo de Retorno:
```json
{
    "message": "Usuário criado com sucesso!"
}
```
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Endpoints Obrigatórios:


#### Livros:

GET /api/v1/books — Lista todos os livros.


Exemplo do Retorno:

```json
[
    {
        "categoria": "Poetry",
        "disponibilidade": 22,
        "preco_com_taxa": 51.77,
        "preco_sem_taxa": 51.77,
        "rating": 3,
        "titulo": "A Light in the Attic"
    },
    {
        "categoria": "Travel",
        "disponibilidade": 19,
        "preco_com_taxa": 45.17,
        "preco_sem_taxa": 45.17,
        "rating": 2,
        "titulo": "It's Only the Himalayas"
    },
```

GET /api/v1/books/<int:book_idx> — Detalhes de um livro pelo índice.


Exemplo de Retorno:

Ao ser inserido o indice 88, foi retornado o livro correspondente:
```json
{
    "categoria": "Fiction",
    "disponibilidade": 15,
    "preco_com_taxa": 21.04,
    "preco_sem_taxa": 21.04,
    "rating": 2,
    "titulo": "Tuesday Nights in 1980",
    "url_imagem": "https://books.toscrape.com/media/cache/a3/ad/a3ade5edecde67449329c1ebb016c049.jpg"
}
```

GET /api/v1/books/search?titulo=(titulo)&categoria=(categoria) — Busca por título/categoria..

Exemplo de Retorno:

Ao ser inserido o título e categoria respectivamente
Behind Closed Doors Thriller

```json
[
    {
        "categoria": "Thriller",
        "disponibilidade": 18,
        "preco_com_taxa": 52.22,
        "preco_sem_taxa": 52.22,
        "rating": 4,
        "titulo": "Behind Closed Doors",
        "url_imagem": "https://books.toscrape.com/media/cache/a5/85/a58571db229f2e8f75ea38861eca7f39.jpg"
    }
]
```

GET /api/v1/categories — Lista todas as categorias.

Exemplo de Retorno:
Retorna todas as categorias de Livros
```json
[
    "Poetry",
    "Travel",
    "Politics",
    "Science Fiction",
    "Thriller",
    "Mystery",
    "Young Adult",
    "Food and Drink",
    "Sequential Art",
    "Nonfiction",
    "Add a comment",
    "Fantasy",
    "Default",
    "Philosophy",
    "Business",
    "Fiction",
    "Historical Fiction",
    "Romance",
    "Humor",
    "Christian",
    "Science",
    "Biography",
    "Health",
    "Christian Fiction",
    "Suspense",
    "Art",
    "Childrens",
    "Music",
    "Historical",
    "Psychology",
    "History",
    "Autobiography",
    "Womens Fiction",
    "Contemporary",
    "Horror",
    "Classics",
    "Religion",
    "Sports and Games",
    "New Adult",
    "Paranormal",
    "Parenting",
    "Adult Fiction",
    "Spirituality",
    "Academic",
    "Self Help",
    "Short Stories",
    "Novels",
    "Cultural",
    "Erotica",
    "Crime"
]
```

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Endpoints Adicionais:

#### Livros Faixa de Preço:
GET /api/v1/books/price-range?min=10&max=50 — Filtra livros por faixa de preço.


Exemplo de retorno:

```json
[
    {
        "categoria": "Mystery",
        "preco_com_taxa": 19.63,
        "titulo": "In a Dark, Dark Wood"
    },
    {
        "categoria": "Nonfiction",
        "preco_com_taxa": 19.83,
        "titulo": "Reskilling America: Learning to Labor in the Twenty-First Century"
    },
    {
        "categoria": "Nonfiction",
        "preco_com_taxa": 22.0,
        "titulo": "In the Country We Love: My Family Divided"
    },
]
```
GET /api/v1/books/top-rated — Lista livros com maior rating.

Exemplo de Retorno:
```json
[
    {
        "categoria": "Science Fiction",
        "preco_com_taxa": 35.67,
        "preco_sem_taxa": 35.67,
        "rating": 5,
        "titulo": "Join"
    },
    {
        "categoria": "Business",
        "preco_com_taxa": 12.61,
        "preco_sem_taxa": 12.61,
        "rating": 5,
        "titulo": "The Third Wave: An Entrepreneur’s Vision of the Future"
    },
    {
        "categoria": "Historical Fiction",
        "preco_com_taxa": 30.25,
        "preco_sem_taxa": 30.25,
        "rating": 5,
        "titulo": "Mrs. Houdini"
    },
    {
        "categoria": "Default",
        "preco_com_taxa": 37.72,
        "preco_sem_taxa": 37.72,
        "rating": 5,
        "titulo": "Done Rubbed Out (Reightman & Bailey #1)"
    },
    {
        "categoria": "Add a comment",
        "preco_com_taxa": 37.4,
        "preco_sem_taxa": 37.4,
        "rating": 5,
        "titulo": "The Song of Achilles"
    },
```

GET /api/v1/stats/overview — Estatísticas gerais.


Exemplo de Retorno:
```json
{
    "distribuicao_ratings": {
        "1": 226,
        "2": 196,
        "3": 203,
        "4": 179,
        "5": 196
    },
    "preco_medio_com_taxa": 35.07,
    "preco_medio_sem_taxa": 35.07,
    "total_livros": 1000
}
```

GET /api/v1/stats/categories — Estatísticas por categoria.

Exemplo de Retorno:
```json
[
    {
        "categoria": "Academic",
        "preco_medio_com_taxa": 13.12,
        "preco_medio_sem_taxa": 13.12,
        "quantidade_livros": 1
    },
    {
        "categoria": "Add a comment",
        "preco_medio_com_taxa": 35.8,
        "preco_medio_sem_taxa": 35.8,
        "quantidade_livros": 67
    },
    {
        "categoria": "Adult Fiction",
        "preco_medio_com_taxa": 15.36,
        "preco_medio_sem_taxa": 15.36,
        "quantidade_livros": 1
    },
]
```
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
### Scraping

POST /api/v1/scraping/trigger — Dispara scraping (JWT).

Exemplo de Retorno:

```json
{
    "message": "Scraping iniciado em background. Consulte o status depois.",
    "status": "processing"
}
```
GET /api/v1/scraping/status — Consulta status do scraping.

Exemplo de Retorno:
```json
{
    "status": "done"
}
```
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Machine Learning
GET /api/v1/ml/features — Dados prontos para features de ML.

Exemplo de Retorno:
```json
[
    {
        "categoria": "Poetry",
        "disponibilidade": 22,
        "preco_com_taxa": 51.77,
        "preco_sem_taxa": 51.77,
        "rating": 3,
        "titulo": "A Light in the Attic"
    },
    {
        "categoria": "Travel",
        "disponibilidade": 19,
        "preco_com_taxa": 45.17,
        "preco_sem_taxa": 45.17,
        "rating": 2,
        "titulo": "It's Only the Himalayas"
    },
    {
        "categoria": "Politics",
        "disponibilidade": 19,
        "preco_com_taxa": 51.33,
        "preco_sem_taxa": 51.33,
        "rating": 2,
        "titulo": "Libertarianism for Beginners"
    },
]
```
GET /api/v1/ml/training-data — Dados para treinamento.


Exemplo de Retorno:
```json
[
    {
        "categoria": "Poetry",
        "disponibilidade": 22,
        "preco_com_taxa": 51.77,
        "preco_sem_taxa": 51.77,
        "rating": 3,
        "titulo": "A Light in the Attic"
    },
    {
        "categoria": "Travel",
        "disponibilidade": 19,
        "preco_com_taxa": 45.17,
        "preco_sem_taxa": 45.17,
        "rating": 2,
        "titulo": "It's Only the Himalayas"
    },
    {
        "categoria": "Politics",
        "disponibilidade": 19,
        "preco_com_taxa": 51.33,
        "preco_sem_taxa": 51.33,
        "rating": 2,
        "titulo": "Libertarianism for Beginners"
    },
    {
        "categoria": "Science Fiction",
        "disponibilidade": 19,
        "preco_com_taxa": 37.59,
        "preco_sem_taxa": 37.59,
        "rating": 1,
        "titulo": "Mesaerion: The Best Science Fiction Stories 1800-1849"
    },
    {
        "categoria": "Poetry",
        "disponibilidade": 17,
        "preco_com_taxa": 33.63,
        "preco_sem_taxa": 33.63,
        "rating": 2,
        "titulo": "You can't bury them all: Poems"
    },
    {
        "categoria": "Thriller",
        "disponibilidade": 18,
        "preco_com_taxa": 52.22,
        "preco_sem_taxa": 52.22,
        "rating": 4,
        "titulo": "Behind Closed Doors"
    },
    {
        "categoria": "Mystery",
        "disponibilidade": 18,
        "preco_com_taxa": 19.63,
        "preco_sem_taxa": 19.63,
        "rating": 1,
        "titulo": "In a Dark, Dark Wood"
    },
]
```
POST /api/v1/ml/predictions — Predição com modelo ML.

Exemplo de Retorno:
```json
[
    {
        "input": {
            "disponibilidade": 1,
            "preco_com_taxa": 10,
            "preco_sem_taxa": 8
        },
        "prediction": 0
    }
]
```
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Logs
GET /api/v1/logs — Retorna logs estruturados (NDJSON).


Exemplo de retorno:
```json
{
        "asctime": "2025-08-10 20:02:20,223",
        "duration": 0.009,
        "levelname": "INFO",
        "message": "request",
        "method": "GET",
        "name": "root",
        "path": "/api/v1/ml/features",
        "remote_addr": "127.0.0.1",
        "request_id": null,
        "status": 200,
        "timestamp": "2025-08-10T23:02:20",
        "user": null
    },
    {
        "asctime": "2025-08-10 20:02:20,224",
        "levelname": "INFO",
        "message": "127.0.0.1 - - [10/Aug/2025 20:02:20] \"GET /api/v1/ml/features HTTP/1.1\" 200 -",
        "name": "werkzeug"
    },
    {
        "asctime": "2025-08-10 20:02:21,292",
        "duration": 0.01,
        "levelname": "INFO",
        "message": "request",
        "method": "GET",
        "name": "root",
        "path": "/api/v1/ml/features",
        "remote_addr": "127.0.0.1",
        "request_id": null,
        "status": 200,
        "timestamp": "2025-08-10T23:02:21",
        "user": null
    },
    {
        "asctime": "2025-08-10 20:02:21,292",
        "levelname": "INFO",
        "message": "127.0.0.1 - - [10/Aug/2025 20:02:21] \"GET /api/v1/ml/features HTTP/1.1\" 200 -",
        "name": "werkzeug"
    },
```

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Scraping

O scraping é disparado manualmente ou automaticamente se o CSV não existir.
Status do scraping pode ser consultado via endpoint.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Machine Learning

O modelo é treinado e carregado automaticamente ao iniciar a API.
Endpoints para features, dados de treino e predição.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Logs

Os logs de execução são salvos em logsExecucao.json no formato NDJSON (um JSON por linha).
Endpoint /api/v1/logs retorna todos os registros.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Monitoramento


Métricas Prometheus disponíveis em /metrics.
