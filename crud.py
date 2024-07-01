from sqlalchemy.orm import Session
import model
import schema

def create_user(db: Session, user: schema.CreateUser):
    db_user = model.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_users(db: Session,  offset: int = 0, limit: int = 10):
    return db.query(model.User).offset(offset).limit(limit).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(model.User).filter(model.User.user_id == user_id).first()

def get_user_by_username(db: Session, username:str):
    return db.query(model.User).filter(model.User.username == username).first()

def UpdateUser(db: Session, username:str, user= schema.UpdateUser):
    db_user = db.query(model.User).filter(model.User.username == username).first()
    if not db_user:
        return None
    db_user.username = user.username
    db_user.email = user.email
    db_user.password_hash = user.password_hash
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    # db.add(db_user)
    db.commit()
    db.refresh(db_user) 
    return db_user    


    