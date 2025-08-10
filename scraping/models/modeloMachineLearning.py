# ml_model.py
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


class MLModel:
    def __init__(self, model_path='meu_modelo.pkl'):
        self.model_path = model_path
        self.model = None

    def treinar(self, df, features, target):
        X = df[features]
        y = df[target]
        self.model = RandomForestClassifier()
        self.model.fit(X, y)
        joblib.dump(self.model, self.model_path)
        print(f"Modelo treinado e salvo em {self.model_path}")

    def carregar(self):
        self.model = joblib.load(self.model_path)
        print(f"Modelo carregado de {self.model_path}")

    def prever(self, X):
        if self.model is None:
            raise Exception("Modelo não carregado!")
        return self.model.predict(X)
