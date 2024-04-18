from flask_openapi3 import Tag

from app import app, db
from app.models.Genres import Genres
from app.models.MangaGenres import MangaGenres
from app.schemas import GenresSchemas, ErrorSchemas

# definindo tag Home
tag = Tag(name="Generos", description="Adição, visualização e remoção de generos da base")


@app.get('/genres', tags=[tag], responses={"200": GenresSchemas.GenreListSchema, "404": ErrorSchemas.ErrorSchema})
def get_genres():
    """
        Faz a busca por todos os Generos cadastrados
        Retorna uma representação da listagem de generos.
    """
    genres = Genres.query.all()

    if not genres:
        return {"mesage": "Nenhum dado encontrado"}, 404
    else:
        result = []
        for genre in genres:
            result.append({
                "id": genre.id,
                "created": genre.created,
                "name": genre.name,
            })

        return {"data": result}, 200


@app.get('/genre', tags=[tag], responses={"200": GenresSchemas.GenreMangaSchema, "404": ErrorSchemas.ErrorSchema})
def get_genre(query: GenresSchemas.GenreSearchSchema):
    """
        Faz a busca por um genero pelo id
        Retorna uma representação do generos.
    """

    genre = Genres.query.filter_by(id=query.id).first()

    if not genre:
        return {"mesage": "Nenhum dado encontrado"}, 404
    else:
        result = {
            "id": genre.id,
            "created": genre.created,
            "name": genre.name,
            "mangas": []
        }

        for manga in genre.mangas:
            manga_data = {
                "id": manga.id,
                "created": manga.created,
                "name": manga.name,
                "description": manga.description,
                "url": manga.url,
                "image": manga.image,
                "status": manga.status,
                "authors": []
            }

            for author in manga.authors:
                manga_data["authors"].append({
                    "id": author.id,
                    "name": author.name,
                })

            result['mangas'].append(manga_data)

        return result, 200


@app.post('/genres', tags=[tag], responses={"201": GenresSchemas.GenreSchema, "400": ErrorSchemas.ErrorSchema, "409": ErrorSchemas.ErrorSchema})
def post_genre(form: GenresSchemas.GenreInsertSchema):
    """
        Insere um novo genero no banco de dados da listagem de generos.
        Retorna uma representação do generos.
    """
    genres = Genres.query.filter(Genres.name == form.name).count()

    if genres:
        return {"mesage": "Genero já cadastrado"}, 409
    else:
        genre = Genres(name=form.name)
        db.session.add(genre)
        if db.session.commit() is None:
            result = {
                "id": genre.id,
                "created": genre.created,
                "name": genre.name
            }
            return {"data": result}, 201
        else:
            return {"mesage": "Não foi possível salvar novo genero"}, 400


@app.put('/genres', tags=[tag], responses={"200": GenresSchemas.GenreSchema, "400": ErrorSchemas.ErrorSchema, "404": ErrorSchemas.ErrorSchema, "409": ErrorSchemas.ErrorSchema})
def put_genre(form: GenresSchemas.GenreUpdateSchema):
    """
        Atualiza um genero no banco de dados da listagem de generos.
        Retorna uma representação do generos.
    """
    genre = Genres.query.filter(Genres.id == form.id).first()

    if not genre:
        return {"mesage": "Nenhum dado encontrado"}, 404
    else:
        genres = Genres.query.filter(Genres.name == form.name).first()
        if genres:
            if genres.id != form.id:
                return {"mesage": "Genero já cadastrado"}, 409

        genre.name = form.name
        if db.session.commit() is None:
            result = {
                "id": genre.id,
                "created": genre.created,
                "name": genre.name
            }
            return {"data": result}, 200
        else:
            return {"mesage": "Não foi possível atualizar o genero"}, 400


@app.delete('/genres', tags=[tag], responses={"200": GenresSchemas.GenreRemoveSchema, "400": ErrorSchemas.ErrorSchema, "404": ErrorSchemas.ErrorSchema})
def delete_genre(query: GenresSchemas.GenreSearchSchema):
    """
        Remove um genero no banco de dados da listagem de generos.
    """
    genre = Genres.query.filter(Genres.id == query.id).first()

    if not genre:
        return {"mesage": "Nenhum dado encontrado"}, 404
    else:
        manga_genres = MangaGenres.query.filter_by(genre_id=genre.id).all()
        for manga_genre in manga_genres:
            db.session.delete(manga_genre)
        if db.session.commit() is None:
            db.session.delete(genre)
            if db.session.commit() is None:
                return {"mesage": "Genero removido"}, 200
            else:
                return {"mesage": "Não foi possível remover o genero"}, 400
        else:
            return {"mesage": "Não foi possível remover o genero"}, 400
