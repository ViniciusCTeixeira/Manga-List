from pydantic import BaseModel
from typing import List
from app.schemas import MangasSchemas


class GenreSchema(BaseModel):
    """ Define como um gênero deve ser representado """
    id: int
    created: str
    name: str


class GenreMangaSchema(BaseModel):
    """ Define como um gênero deve ser representado """
    id: int
    created: str
    name: str
    mangas: list[MangasSchemas.MangaAuthorsSchema]


class GenreInsertSchema(BaseModel):
    """ Define como um novo gênero a ser inserido deve ser representado """
    name: str


class GenreUpdateSchema(BaseModel):
    """ Define como um novo gênero a ser inserido deve ser representado """
    id: int
    name: str


class GenreSearchSchema(BaseModel):
    """ Define como um genero devem ser buscado """
    id: int


class GenreListSchema(BaseModel):
    """ Define como uma lista de gêneros deve ser representada """
    data: List[GenreSchema]


class GenreRemoveSchema(BaseModel):
    """ Define como uma mensagem de erro será representada """
    mesage: str
