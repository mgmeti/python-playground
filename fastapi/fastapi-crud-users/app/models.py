from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy import Integer, String, Column
from app.database import Base

# Sqlalchemy models
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=True)

# Pydantic models
class UserBase(BaseModel):
    name:str
    email: EmailStr
    age: Optional[int] = None

class UserCreate(UserBase):
    pass # Inherits all fields from UserBase

class User(UserBase):
    id:int

    class Cofig:
        orm_mode = True
