from .database import db


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
