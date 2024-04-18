from datetime import datetime

from app import db


class MangaGenres(db.Model):
    __tablename__ = 'manga_genres'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    manga_id = db.Column(db.Integer, db.ForeignKey('mangas.id'))

