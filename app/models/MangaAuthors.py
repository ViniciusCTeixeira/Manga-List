from app import db
from datetime import datetime

class MangaAuthors(db.Model):
    __tablename__ = 'manga_authors'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    manga_id = db.Column(db.Integer, db.ForeignKey('mangas.id'))