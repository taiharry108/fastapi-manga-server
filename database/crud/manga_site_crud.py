from core.manga_site_enum import MangaSiteEnum
from sqlalchemy.orm import Session
from database import models


def create_test_manga_site(db: Session):
    db_manga_site = models.MangaSite(
        name='manhuaren',
        url='https://test.com')
    db.add(db_manga_site)
    db.commit()
    db.refresh(db_manga_site)
    return db_manga_site


def create_manga_site(db: Session, site: MangaSiteEnum):
    from core import manga_site_factory
    url = manga_site_factory.get_manga_site(site).url
    db_manga_site = models.MangaSite(
        name=site.value,
        url=url)
    db.add(db_manga_site)
    db.commit()
    db.refresh(db_manga_site)
    return db_manga_site


def delete_manga_sites(db: Session):
    return db.query(models.MangaSite).delete()


def get_manga_site_id(db: Session, site: MangaSiteEnum) -> int:
    return db.query(models.MangaSite).filter(models.MangaSite.name == site.value).first().id
