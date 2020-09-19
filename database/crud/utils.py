from sqlalchemy.orm import Session


def delete_all(db: Session) -> bool:
    db.query(models.Chapter).delete()
    db.query(models.Manga).delete()
    db.commit()
    return True
