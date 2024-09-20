from flask import Flask
from auth import auth_bp
from home import home_bp
from recipes import recipes_bp
from models import db
from flask_migrate import Migrate

app = Flask(__name__)

# Establecer una clave secreta para manejar sesiones
app.secret_key = 'e13b8c5a9f0c3df88ad9c9e767e0fd41'

# Configurar la base de datos (usando SQLite para este ejemplo)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recetas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos con la aplicación Flask
db.init_app(app)

# Inicializar Flask-Migrate
migrate = Migrate(app, db)

# Crear las tablas si no existen
with app.app_context():
    db.create_all()

app.register_blueprint(home_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(recipes_bp, url_prefix='/recipes')

@app.route('/')
def home():
    return 'Página principal'

if __name__ == "__main__":
    app.run(debug=True)
