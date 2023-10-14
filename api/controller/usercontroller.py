import logging
from sqlalchemy.orm import Session
from api.model import models
from api.database import schemas
import bcrypt
from pydantic import BaseModel,Field
from datetime import datetime

salt = bcrypt.gensalt(8)

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    user =  db.query(models.User).offset(skip).limit(limit).all()
    return user


def create_user(db: Session, user: schemas.UserCreate):
    password = bcrypt.hashpw(user.password.encode('utf-8'), salt)
    db_user = models.User(username=user.username,password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, password: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    newPass = bcrypt.hashpw(password.encode('utf-8'), salt) 
    if user:
        user.password = newPass
        db.commit()
        db.refresh(user)
        return user
    return None

def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()

def get_user_by_username_and_password(db: Session, username: str, password:str):
    # return db.query(models.User).where(models.User.username == username ).first()
    return db.query(models.User).where(models.User.username == username and models.User.password == password ).first()

