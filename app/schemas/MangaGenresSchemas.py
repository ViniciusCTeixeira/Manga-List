from pydantic import BaseModel


class MangaGenresSchema(BaseModel):
    """ Define como um genero devem ser buscado """
    id: int
    created: str


class MangaGenresInsertSchema(BaseModel):
    """ Define como um novo gênero a ser inserido deve ser representado """
    genre: int
    manga: int


class MangaGenresSearchSchema(BaseModel):
    """ Define como um genero devem ser buscado """
    id: int


class MangaGenresMsgSchema(BaseModel):
    """ Define como uma mensagem será representada """
    mesage: str
