import datetime
from pydantic import BaseModel


class OrmModel(BaseModel):
    class Config:
        orm_mode = True


class Comment(OrmModel):
    id: int
    count: int
    checked_at: datetime.datetime


class View(OrmModel):
    id: int
    count: int
    checked_at: datetime.datetime


class Posts(OrmModel):
    board: str
    title: str
    comments: list[Comment] = []
    views: list[View] = []
    created_at: datetime.datetime
