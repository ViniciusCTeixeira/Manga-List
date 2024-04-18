from app import db
from datetime import datetime


class Genres(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    name = db.Column(db.String(255), unique=True)

    mangas = db.relationship('Mangas', secondary='manga_genres', backref=db.backref('manga_genres', lazy='dynamic'),
                             primaryjoin="Genres.id == MangaGenres.genre_id",
                             secondaryjoin="Mangas.id == MangaGenres.manga_id")