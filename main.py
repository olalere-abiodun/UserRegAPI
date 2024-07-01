from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud, model, schema
from database import SessionLocal, engine, Base
from typing import Optional

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/user/")
def create_user(user: schema.CreateUser, db: Session = Depends(get_db)):
    crud.create_user(db, user=user)
    return {"msg": "User created successfully", "user": user}

@app.get("/users/")
def read_users(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    users = crud.get_all_users(db, offset=offset, limit=limit)
    return users

@app.get("/user/id/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



@app.get("/user/username/{username}")
def read_user_by_username(username: str, db:Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/user/Update/{username}")

def update_user(username: str, updated_user: schema.UpdateUser, db: Session = Depends(get_db)):
    user = crud.UpdateUser(db, username, updated_user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user





    

