from pydantic import BaseModel, ConfigDict

# username 
# email
# password_hash
# first_name
# last_name

class UserBase(BaseModel):
    username: str
    email: str
    password_hash: str
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)

class User(UserBase):
    pass

class CreateUser(UserBase):
    pass

class UpdateUser(UserBase):
    pass

