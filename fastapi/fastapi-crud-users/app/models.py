from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id:int
    name:str
    email: EmailStr
    age: Optional[int] = None

class UserCreate(BaseModel):
    name:str
    email: EmailStr
    age: Optional[int] = None
