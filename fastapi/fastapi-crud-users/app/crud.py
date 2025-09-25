from sqlalchemy.orm import Session
from app import models


def create_user(db: Session, user: models.UserCreate):
    db_user = models.UserDB(name=user.name,email=user.email, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.UserDB).filter(models.UserDB.id == user_id).first()

def list_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UserDB).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user_update: models.UserCreate):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.name = user_update.name
        db_user.email = user_update.email
        db_user.age = user_update.age
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id : int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
