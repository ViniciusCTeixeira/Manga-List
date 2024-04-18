import os
from flask_sqlalchemy import SQLAlchemy
from flask_openapi3 import OpenAPI, Info
from flask_cors import CORS


info = Info(title="API para gerencimento de Mangas", version="1.0.0")
instance = os.path.join(os.path.dirname(__file__), 'instance')

app = OpenAPI(__name__, info=info, instance_path=instance)
app.config['LOGS_FOLDER'] = os.path.join(os.path.dirname(__file__), 'logs')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

from app.controllers import HomeController, GenresController, MangasController, AuthorsController, MangaGenresController, MangaAuthorsController
