from flask import redirect
from flask_openapi3 import Tag
from app import app

# definindo tag Home
tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")

@app.get('/', tags=[tag], summary="OpenAPI")
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')