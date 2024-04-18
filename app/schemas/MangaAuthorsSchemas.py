from pydantic import BaseModel


class MangaAuthorSchema(BaseModel):
    """ Define como um genero devem ser buscado """
    id: int
    created: str


class MangaAuthorInsertSchema(BaseModel):
    """ Define como um novo gênero a ser inserido deve ser representado """
    author: int
    manga: int


class MangaAuthorSearchSchema(BaseModel):
    """ Define como um genero devem ser buscado """
    id: int


class MangaAuthorMsgSchema(BaseModel):
    """ Define como uma mensagem será representada """
    mesage: str
