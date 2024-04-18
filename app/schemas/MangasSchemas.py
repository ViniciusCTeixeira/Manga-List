from pydantic import BaseModel
from typing import List


class MangaSchema(BaseModel):
    """ Define como um manga deve ser representado """
    id: int
    created: str
    name: str
    description: str
    url: str
    image: str
    status: int


class MangaGenreAuthorSchema(BaseModel):
    id: int
    name: str

class MangaGenreAuthorsSchema(BaseModel):
    """ Define como um manga com genero deve ser representado """
    id: int
    created: str
    name: str
    description: str
    url: str
    image: str
    status: int
    genres: List[MangaGenreAuthorSchema]
    authors: List[MangaGenreAuthorSchema]


class MangaGenreSchema(BaseModel):
    """ Define como um manga com genero deve ser representado """
    id: int
    created: str
    name: str
    description: str
    url: str
    image: str
    status: int
    genres: List[MangaGenreAuthorSchema]


class MangaAuthorsSchema(BaseModel):
    """ Define como um manga com genero deve ser representado """
    id: int
    created: str
    name: str
    description: str
    url: str
    image: str
    status: int
    authors: List[MangaGenreAuthorSchema]


class MangaInsertSchema(BaseModel):
    """ Define como um novo manga a ser inserido deve ser representado """
    name: str
    name: str
    description: str
    url: str
    image: str
    status: int


class MangaUpdateSchema(BaseModel):
    """ Define como um novo gênero a ser inserido deve ser representado """
    id: int
    name: str
    description: str
    url: str
    image: str
    status: int


class MangaSearchSchema(BaseModel):
    """ Define como um genero devem ser buscado """
    id: int


class MangaListSchema(BaseModel):
    """ Define como uma lista de gêneros deve ser representada """
    data: List[MangaGenreAuthorsSchema]


class MangaRemoveSchema(BaseModel):
    """ Define como uma mensagem de erro será representada """
    mesage: str