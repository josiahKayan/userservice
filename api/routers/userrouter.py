import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.controller import usercontroller
from api.database import database,schemas
from api.model import models
from api.database.database import SessionLocal
from typing import List 

router = APIRouter()

@router.post("/users/", response_model=schemas.User)  # Use the Pydantic model
def create_user(user: schemas.UserCreate):
    logging.warning(user)    
    db = SessionLocal()
    db_user = usercontroller.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user = models.User(username=user.username,password=user.password)
    return usercontroller.create_user(db=db, user=user)

@router.get("/users/", response_model=List[schemas.UserBase])  # Use a list of Pydantic model as the response
# @router.get("/users/", response_model=List[schemas.UserSecret])  # Use a list of Pydantic model as the response
def list_users(skip: int = 0, limit: int = 10):
    db = SessionLocal()
    users = usercontroller.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/id/{user_id}", response_model=schemas.UserSecret)  # Use the Pydantic model
def read_user_by_id(user_id: int):
    db = SessionLocal()
    db_user = usercontroller.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/username/{username}", response_model=schemas.UserSecret)  # New route to get user by username
def read_user_by_username(username: str):
    db = SessionLocal()
    db_user = usercontroller.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=schemas.UserSecret)  # Use the Pydantic model
def update_user( user_id: int,new_password):
    db = SessionLocal()
    return usercontroller.update_user(db=db, user_id=user_id, password=new_password)

@router.delete("/users/{user_id}", response_model=schemas.UserSecret)  # Use the Pydantic model
def delete_user(user_id: int):
    db = SessionLocal()
    db_user = usercontroller.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/users/validateUser", response_model=schemas.UserBase)  # Use the Pydantic model
def validate_user(user: schemas.UserBase):
    logging.warning('Chegou aqui')    
    logging.warning(user.username)    
    db = SessionLocal()
    db_user = usercontroller.get_user_by_username_and_password(db, username=user.username,password=user.password)
    logging.warning(db_user)    
    logging.warning(db_user.username)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Username is not exists")
    return db_user