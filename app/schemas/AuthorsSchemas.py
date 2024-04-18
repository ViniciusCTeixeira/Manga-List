from typing import List

from pydantic import BaseModel

from app.schemas import MangasSchemas


class AuthorSchema(BaseModel):
    """ Define como um autor deve ser representado """
    id: int
    created: str
    name: str


class AuthorMangaSchema(BaseModel):
    """ Define como um autor deve ser representado """
    id: int
    created: str
    name: str
    mangas: list[MangasSchemas.MangaGenreSchema]


class AuthorInsertSchema(BaseModel):
    """ Define como um novo autor a ser inserido deve ser representado """
    name: str


class AuthorUpdateSchema(BaseModel):
    """ Define como um novo autor a ser inserido deve ser representado """
    id: int
    name: str


class AuthorSearchSchema(BaseModel):
    """ Define como um autor devem ser buscado """
    id: int


class AuthorListSchema(BaseModel):
    """ Define como uma lista de autors deve ser representada """
    data: List[AuthorSchema]


class AuthorRemoveSchema(BaseModel):
    """ Define como uma mensagem de erro será representada """
    mesage: str
