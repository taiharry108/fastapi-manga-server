from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum, Table
from sqlalchemy.orm import relation, relationship

from .database import Base
from core.manga_index_type_enum import MangaIndexTypeEnum

favorite_table = Table('favorite', Base.metadata,
                       Column('user_id', Integer, ForeignKey(
                              'users.id')),
                       Column('manga_id', Integer, ForeignKey(
                              'mangas.id'))
                       )

history_table = Table('history', Base.metadata,
                      Column('user_id', Integer, ForeignKey(
                          'users.id')),
                      Column('manga_id', Integer, ForeignKey(
                          'mangas.id'))
                      )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")
    fav_mangas = relationship("Manga", secondary=favorite_table)
    history = relationship("Manga", secondary=history_table)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


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


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    page_url = Column(String, index=True, unique=True)
    type = Column(Enum(MangaIndexTypeEnum), index=True)

    manga_id = Column(Integer, ForeignKey("mangas.id"))
    manga = relationship("Manga", back_populates="chapters")
