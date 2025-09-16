from typing import List, Optional
from app.models import User, UserCreate


users_db: List[User] = []
user_id_counter = 1

def create_user(user: UserCreate) -> User:
    global user_id_counter
    new_user = User(id=user_id_counter, **user.model_dump())
    users_db.append(new_user)
    user_id_counter += 1
    return new_user

def get_user(user_id: int) -> Optional[User]:
    return next((user for user in users_db if user.id == user_id), None)

def update_user(user_id: int, user_update: UserCreate) -> Optional[User]:
    user=get_user(user_id)
    if user:
        user.name = user_update.name
        user.email = user_update.email
        user.age = user_update.age
        return user
    return None

def delete_user(user_id: int) -> bool:
    global users_db
    user = get_user(user_id)
    if user:
        users_db = [user for user in users_db if user.id != user_id]
        return True
    return False

def list_users() -> List[User]:
    return users_db
