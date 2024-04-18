from flask_openapi3 import Tag

from app import app, db
from app.models.Authors import Authors
from app.models.MangaAuthors import MangaAuthors
from app.models.Mangas import Mangas
from app.schemas import MangaAuthorsSchemas, ErrorSchemas

# definindo tag Home
tag = Tag(name="Mangas - Autores", description="Adição, visualização e remoção de autores de um manga da base")

@app.post('/mangas/authors', tags=[tag], responses={"201": MangaAuthorsSchemas.MangaAuthorSchema, "400": ErrorSchemas.ErrorSchema, "409": ErrorSchemas.ErrorSchema})
def post_manga_authors(form: MangaAuthorsSchemas.MangaAuthorInsertSchema):
    """
        Insere um novo autor para um manga no banco de dados.
    """
    manga_authors = MangaAuthors.query.filter(MangaAuthors.author_id == form.author, MangaAuthors.manga_id == form.manga).count()

    if manga_authors:
        return {"mesage": "Autor já cadastrada"}, 409
    else:
        author = Authors.query.filter(Authors.id == form.author).first()
        if not author:
            return {"mesage": "Nenhum autor encontrado"}, 404

        manga = Mangas.query.filter_by(id=form.manga).first()
        if not manga:
            return {"mesage": "Nenhum autor encontrado"}, 404

        manga_author = MangaAuthors(manga_id=form.manga, author_id=form.author)
        db.session.add(manga_author)
        if db.session.commit() is None:
            return {"id": manga_author.id, "created": manga_author.created}, 201
        else:
            return {"mesage": "Não foi possível adcionar o autor"}, 400


@app.delete('/mangas/authors', tags=[tag], responses={"200": MangaAuthorsSchemas.MangaAuthorMsgSchema, "400": ErrorSchemas.ErrorSchema, "404": ErrorSchemas.ErrorSchema})
def delete_manga_authors(query: MangaAuthorsSchemas.MangaAuthorSearchSchema):
    """
        Remove um autor de um manga no banco de dados.
    """
    manga_author = MangaAuthors.query.filter(MangaAuthors.id == query.id).first()

    if not manga_author:
        return {"mesage": "Nenhum dado encontrado"}, 404
    else:
        db.session.delete(manga_author)
        if db.session.commit() is None:
            return {"mesage": "Autor removido"}, 200
        else:
            return {"mesage": "Não foi possível remover o autor"}, 400