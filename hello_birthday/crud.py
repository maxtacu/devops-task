from sqlalchemy.orm import Session
from . import models, schemas


def __add_user(db: Session, username: str, dateOfBirth: str):
    user = models.User(username=username, dateOfBirth=dateOfBirth)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def user_exists_in_db(db: Session, username):
    result = db.query(models.User).filter(models.User.username == username).one_or_none()
    return bool(result)

def add_or_update_user(db: Session, username: str, dateOfBirth: str):
    stmt = db.query(models.User).filter(models.User.username == username).one_or_none()
    if stmt:
        stmt.dateOfBirth = dateOfBirth
        db.commit()
    else:
        __add_user(db, username, dateOfBirth)


def get_user_date_of_birth(db: Session, username: str):
    result = db.query(models.User.dateOfBirth).filter(models.User.username == username).one_or_none()
    return result[0] if result else None
