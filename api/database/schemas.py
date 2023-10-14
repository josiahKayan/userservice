from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    password: str

class UserCreate(UserBase):
    pass

class UserSecret(BaseModel):
    username: str
    id: int

class UserUpdate(BaseModel):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True