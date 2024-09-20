from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Receta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dni_paciente = db.Column(db.String(20), nullable=False)
    nombre_apellido = db.Column(db.String(100), nullable=False)
    justificacion = db.Column(db.Text, nullable=False)
    nombre_generico = db.Column(db.String(100), nullable=False)
    nombre_comercial = db.Column(db.String(100))
    indicaciones = db.Column(db.Text)
    
    # Campos adicionales del farmacéutico
    pvp = db.Column(db.String(50))
    cargo_afiliado = db.Column(db.String(50))
    cargo_obra_social = db.Column(db.String(50))
    observaciones = db.Column(db.Text)
    
    # Nuevos campos
    presentacion = db.Column(db.String(100))
    cantidad_envases = db.Column(db.Integer)

class Vademecum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_generico = db.Column(db.String(100), nullable=False)
    nombre_comercial = db.Column(db.String(100), nullable=False)
    presentacion = db.Column(db.String(100), nullable=False)
