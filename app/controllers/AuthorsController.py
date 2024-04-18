from flask_openapi3 import Tag
from app.schemas import AuthorsSchemas, ErrorSchemas
from app.models.Authors import Authors
from app.models.MangaAuthors import MangaAuthors
from app import app, db

# definindo tag Home
tag = Tag(name="Autores", description="Adição, visualização e remoção de autores da base")


@app.get('/authors', tags=[tag], responses={"200": AuthorsSchemas.AuthorListSchema, "404": ErrorSchemas.ErrorSchema})
def get_authors():
    """
        Faz a busca por todos os Autores cadastrados
        Retorna uma representação da listagem de autores.
    """
    authors = Authors.query.all()

    if not authors:
        return {"mesage": "Nenhum dado encontrado"}, 404
    else:
        result = []
        for author in authors:
            result.append({
                "id": author.id,
                "created": author.created,
                "name": author.name,
            })

        return {"data": result}, 200


@app.get('/author', tags=[tag], responses={"200": AuthorsSchemas.AuthorMangaSchema, "404": ErrorSchemas.ErrorSchema})
def get_author(query: AuthorsSchemas.AuthorSearchSchema):
    """
        Faz a busca por um autor pelo id
        Retorna uma representação do autores.
    """

    author = Authors.query.filter_by(id=query.id).first()

    if not author:
        return {"mesage": "Nenhum dado encontrado"}, 404
    else:
        result = {
            "id": author.id,
            "created": author.created,
            "name": author.name,
            "mangas": []
        }

        for manga in author.mangas:
            manga_data = {
                "id": manga.id,
                "created": manga.created,
                "name": manga.name,
                "description": manga.description,
                "url": manga.url,
                "image": manga.image,
                "status": manga.status,
                "genres": []
            }

            for genre in manga.genres:
                manga_data["genres"].append({
                    "id": genre.id,
                    "name": genre.name,
                })

            result['mangas'].append(manga_data)

        return result, 200


@app.post('/authors', tags=[tag], responses={"201": AuthorsSchemas.AuthorSchema, "400": ErrorSchemas.ErrorSchema, "409": ErrorSchemas.ErrorSchema})
def post_author(form: AuthorsSchemas.AuthorInsertSchema):
    """
        Insere um novo autor no banco de dados da listagem de autores.
        Retorna uma representação do autores.
    """
    author = Authors.query.filter(Authors.name == form.name).count()

    if author:
        return {"mesage": "Autor já cadastrado"}, 409
    else:
        author = Authors(name=form.name)
        db.session.add(author)
        if db.session.commit() is None:
            result = {
                "id": author.id,
                "created": author.created,
                "name": author.name
            }
            return {"data": result}, 201
        else:
            return {"mesage": "Não foi possível salvar novo genero"}, 400


@app.put('/authors', tags=[tag], responses={"200": AuthorsSchemas.AuthorSchema, "400": ErrorSchemas.ErrorSchema, "404": ErrorSchemas.ErrorSchema, "409": ErrorSchemas.ErrorSchema})
def put_author(form: AuthorsSchemas.AuthorUpdateSchema):
    """
        Atualiza um autor no banco de dados da listagem de autores.
        Retorna uma representação do autores.
    """
    author = Authors.query.filter(Authors.id == form.id).first()

    if not author:
        return {"mesage": "Nenhum dado encontrado"}, 404
    else:
        authors = Authors.query.filter(Authors.name == form.name).first()
        if authors:
            if authors.id != form.id:
                return {"mesage": "Autor já cadastrado"}, 409

        author.name = form.name
        if db.session.commit() is None:
            result = {
                "id": author.id,
                "created": author.created,
                "name": author.name
            }
            return {"data": result}, 200
        else:
            return {"mesage": "Não foi possível atualizar o genero"}, 400


@app.delete('/authors', tags=[tag], responses={"200": AuthorsSchemas.AuthorRemoveSchema, "400": ErrorSchemas.ErrorSchema, "404": ErrorSchemas.ErrorSchema})
def delete_author(query: AuthorsSchemas.AuthorSearchSchema):
    """
        Remove um autor no banco de dados da listagem de generos.
    """
    author = Authors.query.filter(Authors.id == query.id).first()

    if not author:
        return {"mesage": "Nenhum dado encontrado"}, 404
    else:
        manga_authors = MangaAuthors.query.filter_by(author_id=author.id).all()
        for manga_author in manga_authors:
            db.session.delete(manga_author)
        if db.session.commit() is None:
            db.session.delete(author)
            if db.session.commit() is None:
                return {"mesage": "Autor removido"}, 200
            else:
                return {"mesage": "Não foi possível remover o autor"}, 400
        else:
            return {"mesage": "Não foi possível remover o autor"}, 400
