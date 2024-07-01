from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from database import Base

# user_id
# username 
# email
# password_hash
# first_name
# last_name

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
