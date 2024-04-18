from datetime import datetime

from app import db


class Mangas(db.Model):
    __tablename__ = 'mangas'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text)
    url = db.Column(db.String(255), unique=True)
    image = db.Column(db.String(255), unique=True)
    status = db.Column(db.Integer)

    genres = db.relationship('Genres', secondary='manga_genres', backref=db.backref('manga_genres_m', lazy='dynamic'),
                              primaryjoin="Mangas.id == MangaGenres.manga_id",
                              secondaryjoin="Genres.id == MangaGenres.genre_id")
    authors = db.relationship('Authors', secondary='manga_authors', backref=db.backref('manga_authors_m', lazy='dynamic'),
                              primaryjoin="Mangas.id == MangaAuthors.manga_id",
                              secondaryjoin="Authors.id == MangaAuthors.author_id")