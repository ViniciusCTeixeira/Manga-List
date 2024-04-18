from app import db
from datetime import datetime

class Authors(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    name = db.Column(db.String(255), unique=True)

    mangas = db.relationship('Mangas', secondary='manga_authors', backref=db.backref('manga_authors', lazy='dynamic'),
                             primaryjoin="Authors.id == MangaAuthors.author_id",
                             secondaryjoin="Mangas.id == MangaAuthors.manga_id")