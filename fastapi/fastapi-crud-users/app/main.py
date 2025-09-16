from fastapi import FastAPI, HTTPException
from typing import List
from app.models import User, UserCreate
from app import crud


app = FastAPI(title="User Management API")

@app.post("/v1/users/", response_model=User)
def create_user(user: UserCreate):
    return crud.create_user(user)

@app.get("/v1/users/", response_model=List[User])
def list_users():
    return crud.list_users()

@app.get("/v1/users/{user_id}", response_model=User)
def get_user(user_id: int):
    return crud.get_user(user_id)


@app.put("/v1/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserCreate):
    updated = crud.update_user(user_id, user)
    if not updated:
        return HTTPException(status_code=404, detail="User not found")
    return updated



@app.delete("/v1/users/{user_id}")
def delete_user(user_id: int):
    success = crud.delete_user(user_id)
    if not success:
        return HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

