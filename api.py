from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
import joblib
import subprocess
import os
import numpy as np
from flask import request, jsonify
from scraping.models.modelos import Usuario, Livros
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from scraping.models.database import db
from bs4 import BeautifulSoup
import csv
import pandas as pd
import threading
from api.treinar_modelo import treinar
from scraping.models.modeloMachineLearning import MLModel
from api.treinar_modelo import treinar
import logging
from pythonjsonlogger import jsonlogger
from api.logging_config import setup_logger
from api.logging_middleware import register_logging_hooks
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
metrics = PrometheusMetrics(app)
app.config.from_object('config')


jwt = JWTManager(app)
swagger = Swagger(app)
db.init_app(app)
logger = setup_logger()
register_logging_hooks(app, logger)


@app.route('/')
def home():
    return "hello, Flask testado!"


try:
    df_books = pd.read_csv('scraping/csv/resultado.csv')
except Exception as e:
    # DataFrame genérico caso o arquivo não exista ou dê erro
    df_books = pd.DataFrame({
        'titulo': [],
        'preco_com_taxa': [],
        'preco_sem_taxa': [],
        'rating': [],
        'disponibilidade': [],
        'categoria': [],
        'url_imagem': []
    })
print(os.path.exists('scraping/csv/resultado.csv'))
print(df_books.head())
print(df_books.columns)
print(len(df_books))

MODEL_PATH = 'meu_modelo.pkl'
csv_path = 'scraping/csv/resultado.csv'

features = ['preco_com_taxa', 'preco_sem_taxa', 'disponibilidade']
target = 'rating'
model = joblib.load('meu_modelo.pkl')

# Treina o modelo ao iniciar o Flask
df = pd.read_csv(csv_path)
ml = MLModel(MODEL_PATH)
ml.treinar(df, features, target)  # Treina e salva o modelo
modelTreinado = ml.carregar()  # Carrega o modelo treinado


def inserir_usuario_admin():
    usuario = Usuario(username='admin', password='1234')
    db.session.add(usuario)
    db.session.commit()
    print("Usuário admin inserido com sucesso!")


def importar_livros_do_csv(df):
    # Deleta todos os registros da tabela Livros antes de importar
    Livros.query.delete()
    db.session.commit()
    for _, row in df.iterrows():
        # Converte os preços para float, tratando valores inválidos
        preco_com_taxa = pd.to_numeric(row['preco_com_taxa'], errors='coerce')
        preco_sem_taxa = pd.to_numeric(row['preco_sem_taxa'], errors='coerce')
        disponibilidade = pd.to_numeric(
            row['disponibilidade'], errors='coerce')
        classificacao = pd.to_numeric(row['rating'], errors='coerce')
        livro = Livros(
            titulo=row['titulo'],
            preco_com_taxa=float(preco_com_taxa) if pd.notnull(
                preco_com_taxa) else 0.0,
            preco_sem_taxa=float(preco_sem_taxa) if pd.notnull(
                preco_sem_taxa) else 0.0,
            disponibilidade=int(disponibilidade) if pd.notnull(
                disponibilidade) else 0,
            categoria=row['categoria'],
            classificacao_em_estrelas=int(
                classificacao) if pd.notnull(classificacao) else 0,
            url_imagem=row['url_imagem']
        )
        db.session.add(livro)
    db.session.commit()


def run_scraper():
    status_file = 'scraping_status.txt'
    try:
        # Indica que está processando
        with open(status_file, 'w') as f:
            f.write('processing')

        # Garante que o diretório existe
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        project_root = os.path.dirname(os.path.abspath(__file__))

        # Executa o comando Scrapy via terminal
        result = subprocess.run(
            ['scrapy', 'crawl', 'booksscraper', '-o', csv_path],
            cwd=project_root,
            capture_output=True,
            text=True
        )

        # Verifica se o comando foi bem-sucedido
        if result.returncode == 0 and os.path.exists(csv_path):
            with open(status_file, 'w') as f:
                f.write('done')
            # Carrega o novo CSV e importa para o banco
            try:
                df = pd.read_csv(csv_path)
                importar_livros_do_csv(df)
            except Exception as e:
                print("Erro ao importar livros do CSV")
            return True
        else:
            with open(status_file, 'w') as f:
                f.write('error')
            print("Erro no Scrapy:", result.stderr)
            return False
    except Exception as e:
        with open(status_file, 'w') as f:
            f.write('error')
        print("Exception ao rodar o Scrapy:", e)
        return False


@app.route('/api/v1/books', methods=['GET'])
def retornaLivros():
    """
    Retorna a lista de títulos dos livros.
    ---
    responses:
      200:
        description: Lista de títulos dos livros
        schema:
          type: object
          properties:
            title:
              type: array
              items:
                type: string
    """
    titles = df_books['titulo'].dropna().tolist()
    return jsonify({'titulo': titles})


@app.route('/api/v1/books/<int:book_idx>', methods=['GET'])
def get_book_by_index(book_idx):
    """
    Retorna detalhes completos de um livro específico pelo índice.
    ---
    parameters:
      - name: book_idx
        in: path
        type: integer
        required: true
        description: Índice do livro no DataFrame
    responses:
      200:
        description: Detalhes do livro
        schema:
          type: object
      404:
        description: Livro não encontrado
    """
    if 0 <= book_idx < len(df_books):
        book = df_books.iloc[book_idx].to_dict()
        return jsonify(book)
    else:
        return jsonify({'error': 'Livro não encontrado'}), 404


@app.route('/api/v1/books/search', methods=['GET'])
def search_books():
    """
    Busca livros por título e/ou categoria.
    ---
    parameters:
      - name: title
        in: query
        type: string
        required: false
        description: Título do livro (ou parte dele)
      - name: category
        in: query
        type: string
        required: false
        description: Categoria do livro
    responses:
      200:
        description: Lista de livros encontrados
        schema:
          type: array
          items:
            type: object
    """
    title = request.args.get('titulo', default=None, type=str)
    category = request.args.get('categoria', default=None, type=str)

    filtered = df_books

    if title:
        filtered = filtered[filtered['titulo'].str.contains(
            title, case=False, na=False)]
    if category:
        filtered = filtered[filtered['categoria'].str.contains(
            category, case=False, na=False)]

    books = filtered.to_dict(orient='records')
    return jsonify(books)


@app.route('/api/v1/categories', methods=['GET'])
def get_categories():
    """
    Lista todas as categorias de livros disponíveis.
    ---
    responses:
      200:
        description: Lista de categorias
        schema:
          type: array
          items:
            type: string
    """
    if 'categoria' not in df_books.columns:
        return jsonify([])  # Ou retorne um erro se preferir
    categories = df_books['categoria'].dropna().unique().tolist()
    return jsonify(categories)


@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """
    Verifica status da API e conectividade com os dados.
    Se o CSV não existir, executa o scraping automaticamente.

    ---
    tags:
      - Health Check
    summary: Verifica a saúde do serviço e a disponibilidade dos dados.
    responses:
      200:
        description: API e dados OK
        schema:
          type: object
          properties:
            status:
              type: string
              example: ok
            data_access:
              type: string
              example: ok
      500:
        description: Erro ao acessar dados ou scraping falhou
        schema:
          type: object
          properties:
            status:
              type: string
              example: error
            data_access:
              type: string
              example: scraping_failed
            error:
              type: string
              example: Mensagem de erro detalhada
    """
    try:
        if not os.path.exists(csv_path):
            scraping_ok = run_scraper()
            if not scraping_ok or not os.path.exists(csv_path):
                return jsonify({"status": "error", "data_access": "scraping_failed"}), 500
        pd.read_csv(csv_path, nrows=1)
        return jsonify({"status": "ok", "data_access": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "data_access": "failed", "error": str(e)}), 500
# -------------------------------------------------------
# Endpoints Opcionais da API
# -------------------------------------------------------
# Endpoints de Overview de estatísticas


@app.route('/api/v1/stats/overview', methods=['GET'])
def stats_overview():
    """
    Estatísticas gerais da coleção de livros
    ---
    tags:
      - Estatísticas
    summary: Retorna estatísticas gerais da coleção de livros.
    responses:
      200:
        description: Estatísticas gerais da coleção de livros.
        schema:
          type: object
          properties:
            total_livros:
              type: integer
              example: 100
            preco_medio_com_taxa:
              type: number
              format: float
              example: 23.45
            preco_medio_sem_taxa:
              type: number
              format: float
              example: 21.10
            distribuicao_ratings:
              type: object
              properties:
                "1":
                  type: integer
                  example: 5
                "2":
                  type: integer
                  example: 10
                "3":
                  type: integer
                  example: 30
                "4":
                  type: integer
                  example: 40
                "5":
                  type: integer
                  example: 15
      500:
        description: Erro ao processar as estatísticas.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Mensagem de erro detalhada"
    """
    try:
        df = pd.read_csv(csv_path)
        preco_com_taxa = pd.to_numeric(
            df['preco_com_taxa'].replace(
                '[^0-9.,]', '', regex=True).str.replace(',', '.'),
            errors='coerce'
        )
        preco_sem_taxa = pd.to_numeric(
            df['preco_sem_taxa'].replace(
                '[^0-9.,]', '', regex=True).str.replace(',', '.'),
            errors='coerce'
        )
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        df = df[df['rating'].isin([1, 2, 3, 4, 5])]
        total_livros = len(df)
        preco_medio_com_taxa = float(preco_com_taxa.mean())
        preco_medio_sem_taxa = float(preco_sem_taxa.mean())
        distribuicao_ratings = df['rating'].value_counts(
        ).sort_index().to_dict()
        distribuicao_ratings = {
            str(i): distribuicao_ratings.get(i, 0) for i in range(1, 6)}
        return jsonify({
            "total_livros": total_livros,
            "preco_medio_com_taxa": round(preco_medio_com_taxa, 2),
            "preco_medio_sem_taxa": round(preco_medio_sem_taxa, 2),
            "distribuicao_ratings": distribuicao_ratings
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/stats/categories', methods=['GET'])
def stats_categories():
    """
    Estatísticas detalhadas por categoria
    ---
    tags:
      - Estatísticas
    summary: Retorna estatísticas detalhadas por categoria (quantidade de livros, preços por categoria).
    responses:
      200:
        description: Estatísticas por categoria.
        schema:
          type: array
          items:
            type: object
            properties:
              categoria:
                type: string
                example: "Fiction"
              quantidade_livros:
                type: integer
                example: 12
              preco_medio_com_taxa:
                type: number
                format: float
                example: 23.45
              preco_medio_sem_taxa:
                type: number
                format: float
                example: 21.10
      500:
        description: Erro ao processar as estatísticas.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Mensagem de erro detalhada"
    """
    try:
        # Garante que os preços são float
        df_books['preco_com_taxa'] = pd.to_numeric(
            df_books['preco_com_taxa'].replace(
                '[^0-9.,]', '', regex=True).str.replace(',', '.'),
            errors='coerce'
        )
        df_books['preco_sem_taxa'] = pd.to_numeric(
            df_books['preco_sem_taxa'].replace(
                '[^0-9.,]', '', regex=True).str.replace(',', '.'),
            errors='coerce'
        )

        stats = (
            df_books.groupby('categoria')
            .agg(
                quantidade_livros=('titulo', 'count'),
                preco_medio_com_taxa=('preco_com_taxa', 'mean'),
                preco_medio_sem_taxa=('preco_sem_taxa', 'mean')
            )
            .reset_index()
        )

        result = []
        for _, row in stats.iterrows():
            result.append({
                "categoria": row['categoria'],
                "quantidade_livros": int(row['quantidade_livros']),
                "preco_medio_com_taxa": round(row['preco_medio_com_taxa'], 2),
                "preco_medio_sem_taxa": round(row['preco_medio_sem_taxa'], 2)
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/books/top-rated', methods=['GET'])
def top_rated_books():
    """
    Lista os livros com melhor avaliação (rating mais alto).
    ---
    tags:
      - Livros
    summary: Retorna todos os livros com o maior rating encontrado no catálogo.
    responses:
      200:
        description: Lista de livros com o rating mais alto
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 12
              titulo:
                type: string
                example: "Livro Exemplo"
              autor:
                type: string
                example: "Autor Exemplo"
              categoria:
                type: string
                example: "Ficção"
              preco_com_taxa:
                type: number
                format: float
                example: 29.90
              preco_sem_taxa:
                type: number
                format: float
                example: 27.00
              rating:
                type: integer
                example: 5
      500:
        description: Erro interno do servidor
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao processar a requisição"
    """
    try:
        df = pd.read_csv(csv_path)
        # Converte rating para inteiro, valores inválidos viram NaN
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

        # Filtra apenas ratings válidos (1 a 5)
        df = df[df['rating'].isin([1, 2, 3, 4, 5])]

        # Descobre o rating máximo
        max_rating = df['rating'].max()

        # Filtra os livros com rating máximo
        top_books = df[df['rating'] == max_rating]

        # Converte preços para float, tratando valores inválidos
        df['preco_com_taxa'] = pd.to_numeric(
            df['preco_com_taxa'].replace(
                '[^0-9.,]', '', regex=True).str.replace(',', '.'),
            errors='coerce'
        )
        df['preco_sem_taxa'] = pd.to_numeric(
            df['preco_sem_taxa'].replace(
                '[^0-9.,]', '', regex=True).str.replace(',', '.'),
            errors='coerce'
        )

        # Monta a resposta
        result = []
        for _, row in top_books.iterrows():
            result.append({
                "titulo": row['titulo'],
                "categoria": row['categoria'],
                "preco_com_taxa": float(row['preco_com_taxa']) if pd.notnull(row['preco_com_taxa']) else None,
                "preco_sem_taxa": float(row['preco_sem_taxa']) if pd.notnull(row['preco_sem_taxa']) else None,
                "rating": int(row['rating'])
            })

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/books/price-range', methods=['GET'])
def get_books_by_price_range():
    """
    Filtra livros dentro de uma faixa de preço específica.
    ---
    tags:
      - Livros
    parameters:
      - name: min
        in: query
        type: number
        format: float
        required: true
        description: Preço mínimo do filtro
        example: 10.00
      - name: max
        in: query
        type: number
        format: float
        required: true
        description: Preço máximo do filtro
        example: 50.00
    responses:
      200:
        description: Lista de livros dentro da faixa de preço especificada
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 123
              titulo:
                type: string
                example: "O Senhor dos Anéis"
              autor:
                type: string
                example: "J.R.R. Tolkien"
              preco_com_taxa:
                type: number
                format: float
                example: 35.90
              categoria:
                type: string
                example: "Fantasia"
      400:
        description: Parâmetros inválidos
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Parâmetros min e max são obrigatórios e devem ser números válidos."
      500:
        description: Erro interno do servidor
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao processar a requisição"
    """
    try:
        min_price = request.args.get('min', type=float)
        max_price = request.args.get('max', type=float)
        if min_price is None or max_price is None:
            return jsonify({"error": "Parâmetros min e max são obrigatórios e devem ser números válidos."}), 400

        # Normaliza o campo de preço
        df = df_books.copy()
        df['preco_com_taxa'] = pd.to_numeric(
            df['preco_com_taxa'].replace(
                '[^0-9.,]', '', regex=True).str.replace(',', '.'),
            errors='coerce'
        )

        # Filtra os livros na faixa de preço
        filtered = df[(df['preco_com_taxa'] >= min_price) &
                      (df['preco_com_taxa'] <= max_price)]

        # Monta a resposta
        books = []
        for _, row in filtered.iterrows():
            books.append({
                "titulo": row['titulo'],
                "preco_com_taxa": float(row['preco_com_taxa']),
                "categoria": row['categoria']
            })
        return jsonify(books), 200
    except Exception as e:
        return jsonify({"error": "Erro ao processar a requisição: " + str(e)}), 500


@app.route('/api/v1/scraping/trigger', methods=['POST'])
@jwt_required()
def trigger_scraping():
    """
    Dispara manualmente a rotina de scraping em rbackground e retorna o status da execução.

    ---
    tags:
      - Scraping
    summary: Executa o scraping dos dados manualmente.
    responses:
      200:
        description: Scraping executado com sucesso
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            message:
              type: string
              example: Scraping concluído com sucesso.
      500:
        description: Erro ao executar o scraping
        schema:
          type: object
          properties:
            status:
              type: string
              example: error
            message:
              type: string
              example: Falha ao executar o scraping.
            error:
              type: string
              example: Mensagem de erro detalhada
    """
    try:
        # Dispara o scraping em uma thread separada
        threading.Thread(target=run_scraper).start()
        return jsonify({
            "status": "processing",
            "message": "Scraping iniciado em background. Consulte o status depois."
        }), 202
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Erro inesperado ao iniciar o scraping.",
            "error": str(e)
        }), 500


@app.route('/api/v1/scraping/status', methods=['GET'])
def scraping_status():
    try:
        if os.path.exists('scraping_status.txt'):
            with open('scraping_status.txt') as f:
                status = f.read().strip()
                df = pd.read_csv(csv_path)
                importar_livros_do_csv(df)
        else:
            status = 'Não terminou'
        return jsonify({"status": status})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route('/api/v1/auth/login', methods=['POST'])
def login_user():
    """
    Faz login do usuário e retorna o JWT.
    ---
    tags:
      - Autenticação
    summary: Realiza login e retorna um token JWT.
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username:
                type: string
                example: admin
              password:
                type: string
                example: 1234
    responses:
      200:
        description: Login bem-sucedido, retorna JWT.
        content:
          application/json:
            schema:
              type: object
              properties:
                access_token:
                  type: string
                  example: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
      401:
        description: Credenciais inválidas.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: Invalid credentials
    """
    data = request.get_json()
    user = Usuario.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        # Converter o ID para string
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200
    return jsonify({"error": "Invalid credentials"}), 401


@app.route('/api/v1/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    """
    Renova o token de acesso usando um refresh token válido.
    ---
    tags:
      - Autenticação
    summary: Renova o token de acesso (JWT).
    security:
      - bearerAuth: []
    responses:
      200:
        description: Token renovado com sucesso.
        content:
          application/json:
            schema:
              type: object
              properties:
                access_token:
                  type: string
                  example: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
      401:
        description: Refresh token inválido ou expirado.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: Invalid refresh token
    """
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_token), 200


@app.route('/api/v1/ml/features', methods=['GET'])
def ml_features():
    """
    Retorna os dados dos livros formatados para uso como features em modelos de ML.
    ---
    tags:
      - Machine Learning
    summary: Retorna features para ML
    responses:
      200:
        description: Dados prontos para ML
        schema:
          type: array
          items:
            type: object
    """
    try:
        # Carrega o DataFrame (pode ser df_books ou ler do CSV)
        df = df_books.copy()

        # Seleciona apenas as colunas relevantes para ML
        features = [
            'titulo', 'categoria', 'preco_com_taxa', 'preco_sem_taxa',
            'disponibilidade', 'rating'
        ]
        df = df[features]

        # Remove linhas com valores nulos (opcional, depende do seu modelo)
        df = df.dropna()

        # Se quiser, pode fazer encoding de categorias aqui (exemplo):
        # df['categoria'] = df['categoria'].astype('category').cat.codes

        # Converte para lista de dicionários
        data = df.to_dict(orient='records')
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao preparar features para ML: {str(e)}"}), 500


@app.route('/api/v1/ml/training-data', methods=['GET'])
def ml_training_data():
    """
    Retorna o dataset completo para treinamento de modelos de ML.
    ---
    tags:
      - Machine Learning
    summary: Retorna dados prontos para treinamento de ML
    responses:
      200:
        description: Dataset para treinamento
        schema:
          type: array
          items:
            type: object
      500:
        description: Erro ao preparar o dataset
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        # Carrega o DataFrame (pode ser df_books ou ler do CSV)
        df = df_books.copy()

        # Seleciona as colunas relevantes para o treinamento
        features = [
            'titulo', 'categoria', 'preco_com_taxa', 'preco_sem_taxa',
            'disponibilidade', 'rating'
        ]
        df = df[features]

        # Remove linhas com valores nulos (opcional)
        df = df.dropna()

        # (Opcional) Pré-processamento extra pode ser feito aqui

        # Converte para lista de dicionários
        data = df.to_dict(orient='records')
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao preparar dataset de treinamento: {str(e)}"}), 500


@app.route('/api/v1/ml/predictions', methods=['POST'])
def ml_predictions():
    """
    Recebe features e retorna predições do modelo de ML.
    ---
    tags:
      - Machine Learning
    summary: Realiza predições com o modelo de ML
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: array
            items:
              type: object
    responses:
      200:
        description: Predições realizadas com sucesso
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
      400:
        description: Dados de entrada inválidos
      500:
        description: Erro interno ao realizar predição
    """
    try:
        # Recebe os dados enviados no corpo da requisição
        input_data = request.get_json()
        if not input_data or not isinstance(input_data, list):
            return jsonify({"error": "Entrada deve ser uma lista de objetos com features"}), 400

        # Converte para DataFrame
        import pandas as pd
        df = pd.DataFrame(input_data)

        # (Opcional) Pré-processamento igual ao usado no treinamento
        # Exemplo: df = preprocess(df)

        # Realiza a predição
        # model deve estar carregado previamente
        predictions = model.predict(df)

        # Monta a resposta, convertendo para tipo nativo do Python
        response = []
        for i, pred in enumerate(predictions):
            # Converte para int ou float do Python, se necessário
            if hasattr(pred, 'item'):
                pred_value = pred.item()
            elif isinstance(pred, (int, float)):
                pred_value = pred
            else:
                # fallback para int
                pred_value = int(pred)
            response.append({
                "input": input_data[i],
                "prediction": pred_value
            })

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": f"Erro ao realizar predição: {str(e)}"}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Agora a tabela será criada corretamente
        if Livros.query.count() == 0:
            importar_livros_do_csv(df_books)
        if not Usuario.query.filter_by(username='admin').first():
            inserir_usuario_admin()
        treinar()
    app.run()
