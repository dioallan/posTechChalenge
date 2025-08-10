import pandas as pd
from scraping.models.modeloMachineLearning import MLModel

# Carregue seu dataset


def treinar():
    df = pd.read_csv('scraping/csv/resultado.csv')
    features = ['preco_com_taxa', 'preco_sem_taxa',
                'disponibilidade']  # ajuste conforme seu caso
    target = 'rating'

    ml = MLModel('meu_modelo.pkl')
    ml.treinar(df, features, target)

    print("Modelo treinado e salvo!")
