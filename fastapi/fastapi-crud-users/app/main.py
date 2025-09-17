from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app import models, crud
from app.database import engine, Base, get_db

# Create the database tables (only for dev/demo; in prod use Alembic)
# Next time you change your models (add a column, new table), you just run:
# alembic revision --autogenerate -m "added age column"
# alembic upgrade head
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Management API")

@app.post("/v1/users/", response_model=models.User)
def create_user(user: models.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/v1/users/", response_model=List[models.User])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_users(db, skip=skip, limit=limit)

@app.get("/v1/users/{user_id}", response_model=models.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/v1/users/{user_id}", response_model=models.User)
def update_user(user_id: int, user: models.UserCreate,  db: Session = Depends(get_db)):
    updated = crud.update_user(db, user_id, user)
    if not updated:
        return HTTPException(status_code=404, detail="User not found")
    return updated

@app.delete("/v1/users/{user_id}")
def delete_user(user_id: int,  db: Session = Depends(get_db)):
    success = crud.delete_user(db, user_id)
    if not success:
        return HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

