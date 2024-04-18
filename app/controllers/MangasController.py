from flask_openapi3 import Tag

from app import app, db
from app.models.MangaAuthors import MangaAuthors
from app.models.MangaGenres import MangaGenres
from app.models.Mangas import Mangas
from app.schemas import MangasSchemas, ErrorSchemas

# definindo tag Home
tag = Tag(name="Mangas", description="Adição, visualização e remoção de mangas da base")


@app.get('/mangas', tags=[tag], responses={"200": MangasSchemas.MangaListSchema, "404": ErrorSchemas.ErrorSchema})
def get_mangas():
    """
        Faz a busca por todos os Mangas cadastrados
        Retorna uma representação da listagem de mangas.
    """
    mangas = Mangas.query.all()

    if not mangas:
        return {"mesage": "Nenhum dado encontrado"}, 404
    else:
        result = []
        for manga in mangas:
            manga_data = {
                "id": manga.id,
                "created": manga.created,
                "name": manga.name,
                "description": manga.description,
                "url": manga.url,
                "image": manga.image,
                "status": manga.status,
                "genres": [],
                "authors": [],
            }

            # Adiciona os gêneros do manga ao dicionário
            for genre in manga.genres:
                manga_data["genres"].append({
                    "id": genre.id,
                    "name": genre.name,
                })

            # Adiciona os autores do manga ao dicionário
            for author in manga.authors:
                manga_data["authors"].append({
                    "id": author.id,
                    "name": author.name,
                })

            result.append(manga_data)

        return {"data": result}, 200


@app.get('/manga', tags=[tag], responses={"200": MangasSchemas.MangaGenreAuthorsSchema, "404": ErrorSchemas.ErrorSchema})
def get_manga(query: MangasSchemas.MangaSearchSchema):
    """
        Faz a busca por um manga pelo id
        Retorna uma representação do mangas.
    """

    manga = Mangas.query.filter_by(id=query.id).first()

    if not manga:
        return {"mesage": "Nenhum dado encontrado"}, 404
    else:
        result = {
            "id": manga.id,
            "created": manga.created,
            "name": manga.name,
            "description": manga.description,
            "url": manga.url,
            "image": manga.image,
            "status": manga.status,
            "genres": [],
            "authors": [],
        }
        for genre in manga.genres:
            result["genres"].append({
                "id": genre.id,
                "name": genre.name,
            })
        for author in manga.authors:
            result["authors"].append({
                "id": author.id,
                "name": author.name,
            })

        return result, 200


@app.post('/mangas', tags=[tag], responses={"201": MangasSchemas.MangaSchema, "400": ErrorSchemas.ErrorSchema, "409": ErrorSchemas.ErrorSchema})
def post_mangas(form: MangasSchemas.MangaInsertSchema):
    """
        Insere um novo manga no banco de dados da listagem de mangas.
        Retorna uma representação do mangas.
    """
    mangas = Mangas.query.filter(Mangas.name == form.name).count()

    if mangas:
        return {"mesage": "Manga já cadastrado"}, 409
    else:
        manga = Mangas(name=form.name, url=form.url, image=form.image, status=form.status, description=form.description)
        db.session.add(manga)
        if db.session.commit() is None:
            result = {
                "id": manga.id,
                "created": manga.created,
                "name": manga.name,
                "description": manga.description,
                "url": manga.url,
                "image": manga.image,
                "status": manga.status,
            }
            for genre in manga.genres:
                result["genres"].append({
                    "id": genre.id,
                    "name": genre.name,
                })
            for author in manga.authors:
                result["authors"].append({
                    "id": author.id,
                    "name": author.name,
                })
            return {"data": result}, 201
        else:
            return {"mesage": "Não foi possível salvar novo manga"}, 400


@app.put('/mangas', tags=[tag], responses={"200": MangasSchemas.MangaGenreAuthorsSchema, "400": ErrorSchemas.ErrorSchema, "404": ErrorSchemas.ErrorSchema, "409": ErrorSchemas.ErrorSchema})
def put_mangas(form: MangasSchemas.MangaUpdateSchema):
    """
        Atualiza um genero no banco de dados da listagem de generos.
        Retorna uma representação do generos.
    """
    manga = Mangas.query.filter(Mangas.id == form.id).first()

    if not manga:
        return {"mesage": "Nenhum dado encontrado"}, 404
    else:
        mangas = Mangas.query.filter(Mangas.name == form.name).first()
        if mangas:
            if mangas.id != form.id:
                return {"mesage": "Manga já cadastrado"}, 409

        manga.name = form.name
        manga.description = form.description
        manga.url = form.url
        manga.image = form.image
        manga.status = form.status
        if db.session.commit() is None:
            result = {
                "id": manga.id,
                "created": manga.created,
                "name": manga.name,
                "description": manga.description,
                "url": manga.url,
                "image": manga.image,
                "status": manga.status,
                "genres": [],
                "authors": [],
            }
            for genre in manga.genres:
                result["genres"].append({
                    "id": genre.id,
                    "name": genre.name,
                })
            for author in manga.authors:
                result["authors"].append({
                    "id": author.id,
                    "name": author.name,
                })
            return {"data": result}, 200
        else:
            return {"mesage": "Não foi possível atualizar o manga"}, 400



@app.delete('/mangas', tags=[tag], responses={"200": MangasSchemas.MangaRemoveSchema, "400": ErrorSchemas.ErrorSchema, "404": ErrorSchemas.ErrorSchema})
def delete_mangas(query: MangasSchemas.MangaSearchSchema):
    """
        Remove um genero no banco de dados da listagem de generos.
    """
    manga = Mangas.query.filter(Mangas.id == query.id).first()

    if not manga:
        return {"mesage": "Nenhum dado encontrado"}, 404
    else:
        manga_genres = MangaGenres.query.filter_by(manga_id=manga.id).all()
        manga_authors = MangaAuthors.query.filter_by(manga_id=manga.id).all()
        for manga_genre in manga_genres:
            db.session.delete(manga_genre)
        for manga_author in manga_authors:
            db.session.delete(manga_author)
        if db.session.commit() is None:
            db.session.delete(manga)
            if db.session.commit() is None:
                return {"mesage": "Manga removido"}, 200
            else:
                return {"mesage": "Não foi possível remover o Manga"}, 400
        else:
            return {"mesage": "Não foi possível remover o Manga"}, 400
