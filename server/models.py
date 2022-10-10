from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, Integer, String, Date, text, ForeignKey

from database import Base


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    board = Column(String)
    title = Column(String)
    created_at = Column(DateTime())
    comments = relationship("Comments", backref="posts")
    views = relationship("Views", backref="posts")


class CountHistoryMixin(object):
    id = Column(Integer, primary_key=True, index=True)
    count = Column(Integer)
    checked_at = Column(DateTime(), server_default=text("NOW()"))

    @declared_attr
    def ppomppu_id(cls):
        return Column(Integer, ForeignKey("posts.id"))


class Comments(CountHistoryMixin, Base):
    __tablename__ = "comments"


class Views(CountHistoryMixin, Base):
    __tablename__ = "views"
