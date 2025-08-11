# posTechChalenge
Repositorio TechChalengeFiap

API RESTful para gerenciamento, consulta e análise de livros, com scraping, autenticação JWT, estatísticas, integração com Prometheus, endpoints para Machine Learning e logging estruturado.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Instalacao](#instalacao)
- [Configuracao](#configuracao)
- [Autenticacao e criacao de Usuarios](#autenticacao-e-criacao-de-usuarios)
- [Scraping](#scraping)
- [Machine Learning](#machine-learning)
- [Sistema de Autenticacao JWT](#autenticacao-e-criacao-de-usuarios)
    - [JWT Geracao de Token](#jwt-geracao-de-token)
    - [JWT Refresh Token](#jwt-refresh-token)
    - [JWT Criacao de Usuario](#jwt-criacao-de-usuario)
- [Execucao Scraping](#execucao-scraping)
    - [Disparo Trigger Scraping](#disparo-trigger-scraping)
    - [Status Trigger Scraping](#status-trigger-scraping)
- [Endpoints Obrigatorios Core](#sistema-de-autenticacao-jwt)
    - [Livros Lista](#livros-lista)
    - [Livros Indice](#livros-indice)
    - [Livros Busca Titulo e Categoria](#livros-busca-titulo-e-categoria)
    - [Livros Lista Categorias](#livros-lista-categorias)
- [Endpoints Adicionais Insights](#endpoints-adicionais-insights)
    - [Livros Faixa de Preco](#livros-faixa-de-preco)
    - [Livros Lista Maior Rating](#livros-lista-maior-rating)
    - [Livros Estatisticas Gerais](#livros-estatisticas-gerais)
    - [Livros Estatisticas Categoria](#livros-estatisticas-categoria)
- [Endpoints Machine Learning](#endpoints-machine-learning)
    - [ML Predicoes](#ml-predicoes)
    - [ML Features](#ml-features)
    - [ML Treinamento Dados](#ml-treinamento-dados)
- [Logs](#logs)
    - [Logs via console e arquivo .json](#logs-via-console-e-arquivo-json)
    - [Logs via Prometheus](#logs-via-prometheus) 
- [Dashboard Monitoramento](#dashboard-monitoramento)
    - [Dashboard Metricas Prometheus](#dashboard-metricas-prometheus)
    - [Dashboard Logs Estruturados](#dashboard-logs=estruturados)
- [Documentacao Interativa](#documentacao-interativa)


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

CRUD de livros (via scraping e importação). - [Disparo Trigger Scraping](#disparo-trigger-scraping) 
Busca por título, categoria e faixa de preço. - [Endpoints Obrigatorios Core](#sistema-de-autenticacao-jwt)
Estatísticas gerais e por categoria. - [Endpoints Adicionais Insights](#endpoints-adicionais-insights)
Endpoints para consumo e predição de modelos de Machine Learning. - [Endpoints Machine Learning](#endpoints-machine-learning)
Autenticação JWT. - [Sistema de Autenticacao JWT](#autenticacao-e-criacao-de-usuarios)
Logging estruturado. - [Logs](#logs)
Swagger UI para documentação interativa. - [Documentacao Interativa](#documentacao-interativa)

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Instalacao

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

## Configuracao

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

## Autenticacao e criacao de Usuarios:

Por padrão é criado o usuário admin e senha 1234, para testes de autenticação via JWT, tendo as rotas 'login' - Geração de Token, refresh para renovação de token
e 'newuser', para criação de novo usuário.
Nessa Api, a autenticação via JWT é obrigatória somente nas requisições para criação de novos usuários 'newuser' e 'trigger', para executar o scrapping e fazer
a carga no Dataframe e Database.

Para mais detalhes e exemplos de rotas JWT: [Autenticaçao JWT](#autenticacao-jwt)

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Scraping

O Scraping é disparado através da rota api/v1/scraping/trigger, esse por sua vez exige autenticação, e é feita a coleta do site https://books.toscrape.com/, o resultado é formatado e salvo em 
um CSV: com os campos Título, Categoria, Raiting, Disponibilidade, Preço com taxa e Preço sem taxa, na execução da API, são extraidos os dados para um DataFrame Pandas, e feito uma cópia (BKP)
em uma Tabela do Banco de Dados TechChalenge.db

Detalhes e exemplos da Execução via Scraping: - [Disparo Trigger Scraping](#disparo-trigger-scraping)


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


## Machine Learning

O modelo é treinado e carregado automaticamente ao iniciar a API, através do método 'Treinar', que gera o arquivo meu_modelo.pkl, 
através do dataframe coletado, esses dados são treinados para devolver estimativas que ajudam conforme o objetivo do usuário,
nessa api, tem alguns endpoints básicos de exemplo que testam essa funcionalidade, através do guia de endpoints:

Endpoints para features, dados de treino e predição. - [Endpoints Machine Learning](#endpoints-machine-learning)


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Sistema de Autenticacao JWT

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Fluxo de validações de Credenciais, algumas rotas sensíveis da api são prottegidas pelo método de autenticação JWT, o desenho ilustra uma chamada rest, e o fluxo que acessa as credenciais para
validação, exemplos onde serão utilizadas, no processo de carga do scraping, e criação de novos usuários.

![Desenho Usuário](images/rota_usuario.jpg)

### JWT Geracao de Token

POST /api/v1/auth/login — Login e obtenção de token JWT.

Demonstração do endereço de chamda via postman, onde é utilizado o método POST, e passando os atributos de entrada.

![Desenho Usuário](images/jwt-login.jpg)

Exemplo de Entrada Texto:
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

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### JWT Refresh Token

POST /api/v1/auth/refresh — Renovação do token de acesso.

Demonstração do método post de refresh do token, onde no postman, o preenchimento dos atributos de entradas para requisição é no Headers > Key (Selecionar 'Authorization'), 
Value, preencher com Bearer, um espaço e colar o 'refresh_token', gerado na requisição anterior de login.

![Desenho Usuário](images/jwt-login.jpg)

Exemplo de Entrada Texto:

```json
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NDgwMzI2OSwianRpIjoiMGZkMGY5YTQtOWZjYS00YmM5LWJjODgtMDRmNzQ5MWZjYjAyIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiIxIiwibmJmIjoxNzU0ODAzMjY5LCJjc3JmIjoiZjA5NDNlZDUtOGY2OS00OTI4LWJjNmItYTNmYTE4MDU4OWE2IiwiZXhwIjoxNzU3Mzk1MjY5fQ.TFnji2dem9OIveGRVGODCxGL0dnD8iYySwkof7Te8kQ
```
Exemplo de Retorno:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NDg4Mzg1OCwianRpIjoiMDEwN2ViNWYtYmVkYi00NjYwLWFjYjUtODY1ZDJlZTlkOTljIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NTQ4ODM4NTgsImNzcmYiOiIzNWY1OGVhNi0xYzQxLTQ1YzItOTEyYS0zNGFlNjY5NWNhN2IiLCJleHAiOjE3NTQ4ODQ3NTh9.pNqYSXrZS14bnEb-AJ6mWasQw13fklTXKmHONph300w"
}
```

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### JWT Criacao de Usuario


POST /api/v1/auth/newuser — Criação de novo usuário (JWT).

Desenho do fluxo de criação de novo usuário:


Exemplo de cadastro de novo usuário, com o exemplo da entrada, e nesse caso é obrigatório fazer a autenticação JWT, no postman, o caminho é Authorization > Bearer Token > e colar o 
'access_token', gerado na etapa de login.

![Desenho Usuário](images/jwt-usernew.jpg)

Exemplo de Entrada Texto:

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

## Endpoints Obrigatorios Core:

Desenho Macro do fluxo de chamdas Rest da api, todas as chamadas seguem basicamente esse fluxo, é feita o POST ou GET, 
a api consulta o DataFrame e devolve a requisição para o usuário

![Desenho Usuário](images/rota_usuario.jpg)

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Livros Lista:

GET /api/v1/books — Lista todos os livros.

Exemplo de solicitação no postman, para chamada do metodo Get, onde é listado todos os registros do Dataframe.

![Desenho Usuário](images/livros-features.jpg)


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
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Livros Indice:

GET /api/v1/books/<int:book_idx> — Detalhes de um livro pelo índice.

Exemplo de chamada via postman, onde o método Get faz a busca na lista pelo indice 888.

![Desenho Usuário](images/livros-indice.jpg)


Exemplo de Retorno:

Ao ser inserido o indice 888, foi retornado o livro correspondente:
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
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Livros Busca Titulo e Categoria:

GET /api/v1/books/search?titulo=(titulo)&categoria=(categoria) — Busca por título/categoria.

Exemplo de chamada via postman, onde o método Get faz a busca na lista pelo título e categoria, que no caso foram 
'Behind Closed Doors Thriller' e 'Thriller'.

![Desenho Usuário](images/livros-titulo.jpg)

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

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Livros Lista Categorias:

GET /api/v1/categories — Lista todas as categorias.

Exemplo de chamada via postman, onde o método Get faz a busca de todas as categorias presentes no DataFrame:

![Desenho Usuário](images/livros-categorias.jpg)

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

## Endpoints Adicionais Insights:

O Mesmo desenho Macro do fluxo de chamadas Rest da api, segue o mesmo padrão onde é feita o POST ou GET, 
a api consulta o DataFrame e devolve a requisição para o usuário

![Desenho Usuário](images/rota_usuario.jpg)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Livros Faixa de Preco:

GET /api/v1/books/price-range?min=10&max=50 — Filtra livros por faixa de preço.

Chamada via postman, onde o método Get faz a busca do range de preços minimo 10 e máximo 50

![Desenho Usuário](images/estatistica-range.jpg)

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
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Livros Lista Maior Rating

GET /api/v1/books/top-rated — Lista livros com maior rating.

Chamada via postman, onde o método Get faz retorna os livros classificados maior Rating

![Desenho Usuário](images/estatistica-toprated.jpg)

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

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Livros Estatisticas Gerais:

GET /api/v1/stats/overview — Estatísticas gerais.

Chamada via postman, onde o método Get faz retorna Estatisticas Gerais da lista.

![Desenho Usuário](images/estatistica-gerais.jpg)


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

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Livros Estatisticas Categoria:

GET /api/v1/stats/categories — Estatísticas por categoria.

Chamada via postman, onde o método Get faz retorna Estatisticas por categoria do livro presente na lista.

![Desenho Usuário](images/estatistica-categoria.jpg)

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

## Endpoints Machine Learning

Nessa etapa temos os Endpoints para features, dados de treino e predição, onde nos metodos de predição e features, é feita a coleta dos dados, através do modelo gerado
e o Treino, é a execução conforme o que ele aprendeu devolvendo um resultado conforme as estimativas.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## ML Features

GET /api/v1/ml/features — Predição com modelo ML.

Método Get, exemplo no postman, que retorna as features para treinamento para o modelo.

![Desenho Usuário](images/ML-features.jpg)

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

## ML Predicoes

POST /api/v1/ml/predictions — Predição com modelo ML.

Método POST, onde é inserido valores para predições, que o modelo usará para treinamento e processamento no método de treinamento.

![Desenho Usuário](images/ML-predictions.jpg)

Exemplo de Entrada Texto:
```json
[
  {
    "preco_com_taxa": 10,
    "preco_sem_taxa": 8,
    "disponibilidade": 1
  }
]
```


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

## ML Treinamento Dados

GET /api/v1/ml/training-data — Dados para treinamento.

Método GET, que retorna valores conforme o treimamento e estimativas dos métodos anteriores.

![Desenho Usuário](images/ML-training.jpg)

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

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Execucao Scraping

Desenho Macro do fluxo de chamada via Scraping, rota protegida JWT, onde o usuário faz a solicitação, após a autenticação é feita a coleta de dados do site, gravados em um arquivo .csv
e usado por meio de Dataframe pela Api, automaticamente ao fazer o scraping, é feita uma cópia (Backup) em um banco de dados, garantindo assim, uma possível reutilização, em caso de perda
de dados, ou site de origem fora do ar.

![Desenho Usuário](images/rotas-scraping.jpg)

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Disparo Trigger Scraping:

POST /api/v1/scraping/trigger — Dispara scraping (JWT).

Exemplo no Postman, um método Post, que exige autenticação JWT por ser uma rota sensivel, que roda em Background, já que o processo de coleta de dados leva em media 
uns 15 minutos, após a coleta uma rotina pega os dados do .CSV e atualiza a tabela de banco de dados (Backup),enquando executa ele gera um arquivo scraping_status.txt,
que fica com status 'processing', e quando conclui, esse valor é alterado para 'done'.

![Desenho Usuário](images/scraping-trigger.jpg)


Exemplo de Retorno:

```json
{
    "message": "Scraping iniciado em background. Consulte o status depois.",
    "status": "processing"
}
```

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Status Trigger Scraping:

GET /api/v1/scraping/status — Consulta status do scraping.

Método Get, que retorna o status do processo do scraping disparado anteriormente, esse fica em 'done', quando concluir

![Desenho Usuário](images/scraping-status.jpg)
Exemplo de Retorno:
```json
{
    "status": "done"
}
```


## ML Features

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

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Logs

Esssa Api, está gerando logs de duas formas, tanto pelo proprio python, gerando um arquivo de logs de todas as chamadas, e também em real-time via console,
quanto no Prometheus, esses dois logs podem ser consultados depois via Streamlit, em um Dashboard Unificado.

Endpoint /api/v1/logs retorna todos os registros.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Logs via console e arquivo json

GET /api/v1/logs retorna todos os registros.

Desenho do fluxo de gravação de logs:

![Desenho Usuário](images/logs.jpg)

Essa chamada retorna os logs gravados no arquivo, com os endpoints, horario, código de retorno.

![Desenho Usuário](images/logs-json.jpg)

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Logs via Prometheus

GET (http://127.0.0.1:5000/metrics) retorna todos os registros coletados pelo Prometheus:

Essa chamada retorna os logs gravados no arquivo, com os endpoints, horario, código de retorno e aLatencia, facilitando a monitoração dos registros:

Exemplo de chamada:

![Desenho Usuário](images/logs-prometheus.jpg)


Exemplo de Retorno:

```json
flask_http_request_duration_seconds_bucket{le="0.005",method="GET",path="/api/v1/books/888",status="200"} 2.0
flask_http_request_duration_seconds_bucket{le="0.01",method="GET",path="/api/v1/books/888",status="200"} 2.0
flask_http_request_duration_seconds_bucket{le="0.025",method="GET",path="/api/v1/books/888",status="200"} 2.0
flask_http_request_duration_seconds_bucket{le="0.05",method="GET",path="/api/v1/books/888",status="200"} 2.0
flask_http_request_duration_seconds_bucket{le="0.075",method="GET",path="/api/v1/books/888",
```

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Dashboard Monitoramento

Para o monitoramento da api foi utilizado o streamlit, que coleta os dados do prometheus e os logs estruturados gerados no json, e monta um dashboard final com dados como tempo de execução
métricas, latencias:

Essa execução tem que ser feita via terminal através do seguinte comando bash:

```bash
streamlit run apis/dashboardUnificado.py
```
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Dashboard Metricas Prometheus:

Exibição das Métricas coletadas pelo Prometheus das chamadas feitas via api:

![Desenho Usuário](images/dashboard-prometheus.jpg)


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Dashboard Logs Estruturados:

Exibição das Métricas e calculos de chamadas, tempo de execução, resposta e latência da aplicação:

![Desenho Usuário](images/logs-estruturado.jpg)

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Documentacao Interativa

Documentação estruturada, Flask, com os endpoints e sua descrição, como chamadas, retornos, separados por categorias, seguindo o enunciado do TechChalenge:
- Desafio Adicional (Bônus) - Autenticação, com os endpoints, /api/v1/auth/login, /api/v1/auth/newuser e /api/v1/auth/refresh.
- Endpoints Obrigatórios da API - Endpoints Core, /api/v1/books/price-range, /api/v1/books/top-rated, /api/v1/stats/categories e ​/api​/v1​/stats​/overview.
- Logs, /api/v1/logs
- Pipeline Machine Learning-Ready, /api/v1/ml/features, /api/v1/ml/predictions e /api/v1/ml/training-data
- Scraping, /api/v1/scraping/status e /api/v1/scraping/trigger

![Desenho Usuário](images/apidocs-1.jpg)

![Desenho Usuário](images/apidocs-2.jpg)

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------