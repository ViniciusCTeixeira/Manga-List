from flask_openapi3 import Tag

from app import app, db
from app.models.Genres import Genres
from app.models.MangaGenres import MangaGenres
from app.models.Mangas import Mangas
from app.schemas import MangaGenresSchemas, ErrorSchemas

# definindo tag Home
tag = Tag(name="Mangas - Generos", description="Adição, visualização e remoção de generos de um manga da base")

@app.post('/mangas/genres', tags=[tag], responses={"201": MangaGenresSchemas.MangaGenresSchema, "400": ErrorSchemas.ErrorSchema, "409": ErrorSchemas.ErrorSchema})
def post_manga_genres(form: MangaGenresSchemas.MangaGenresInsertSchema):
    """
        Insere um novo genero para um manga no banco de dados.
    """
    manga_genres = MangaGenres.query.filter(MangaGenres.genre_id == form.genre, MangaGenres.manga_id == form.manga).count()

    if manga_genres:
        return {"mesage": "Genero já cadastrada"}, 409
    else:
        genre = Genres.query.filter(Genres.id == form.genre).first()
        if not genre:
            return {"mesage": "Nenhum genero encontrado"}, 404

        manga = Mangas.query.filter_by(id=form.manga).first()
        if not manga:
            return {"mesage": "Nenhum manga encontrado"}, 404

        manga_genre = MangaGenres(manga_id=form.manga, genre_id=form.genre)
        db.session.add(manga_genre)
        if db.session.commit() is None:
            return {"id": manga_genre.id, "created": manga_genre.created}, 201
        else:
            return {"mesage": "Não foi possível adcionar o genero"}, 400


@app.delete('/mangas/genres', tags=[tag], responses={"200": MangaGenresSchemas.MangaGenresMsgSchema, "400": ErrorSchemas.ErrorSchema, "404": ErrorSchemas.ErrorSchema})
def delete_manga_genres(query: MangaGenresSchemas.MangaGenresSearchSchema):
    """
        Remove um genero de um manga no banco de dados.
    """
    manga_genre = MangaGenres.query.filter(MangaGenres.id == query.id).first()

    if not manga_genre:
        return {"mesage": "Nenhum dado encontrado"}, 404
    else:
        db.session.delete(manga_genre)
        if db.session.commit() is None:
            return {"mesage": "Genero removido"}, 200
        else:
            return {"mesage": "Não foi possível remover o genero"}, 400