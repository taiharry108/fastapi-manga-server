from enum import unique
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum, Table
from sqlalchemy.orm import relationship

from .database import Base
from core.manga_index_type_enum import MangaIndexTypeEnum

favorite_table = Table('favorite', Base.metadata,
                       Column('user_id', Integer, ForeignKey(
                              'users.id')),
                       Column('manga_id', Integer, ForeignKey(
                              'mangas.id'))
                       )


class History(Base):
    __tablename__ = 'history'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    manga_id = Column(Integer, ForeignKey('mangas.id'), primary_key=True)
    last_added = Column(DateTime)
    manga = relationship("Manga", back_populates="users")
    user = relationship("User", back_populates="history_mangas")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    fav_mangas = relationship("Manga", secondary=favorite_table)
    history_mangas = relationship("History", back_populates="user")


class MangaSite(Base):
    __tablename__ = "manga_sites"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    url = Column(String, index=True, unique=True)

    mangas = relationship("Manga", back_populates="manga_site")


class Manga(Base):
    __tablename__ = "mangas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    url = Column(String, index=True, unique=True)
    last_update = Column(DateTime, index=True)
    finished = Column(Boolean)
    thum_img = Column(String, index=True)
    chapters = relationship("Chapter", back_populates="manga")
    manga_site_id = Column(Integer, ForeignKey("manga_sites.id"))
    manga_site = relationship("MangaSite", back_populates="mangas")
    users = relationship("History", back_populates="manga")


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    page_url = Column(String, index=True, unique=True)
    type = Column(Enum(MangaIndexTypeEnum), index=True)

    manga_id = Column(Integer, ForeignKey("mangas.id"))
    manga = relationship("Manga", back_populates="chapters")
    pages = relationship("Page", back_populates="chapter")


class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"))
    chapter = relationship("Chapter", back_populates="pages")
    pic_path = Column(String, index=True, unique=True)
    idx = Column(Integer, index=True)
