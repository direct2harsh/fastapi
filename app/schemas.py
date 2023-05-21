from pydantic import BaseModel,EmailStr
from datetime import datetime

# This post is from pydentic/schema model defines the structure of request and response
# if the field in the model are not present during request then it will not execute the request
# This makes the code typesafe


    

class PostBase(BaseModel):
    title : str
    content :str
    published : bool = True

class CreatePost(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created : datetime
    #This config is to tell pydantic to read data even if the data is not dictionay 
    # By default pydantic expects the data to be dictionay but in our case we are using ORM 
    class Config():
        orm_mode = True

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    email:EmailStr
    id:int
    created:datetime
    #This config is to tell pydantic to read data even if the data is not dictionay 
    # By default pydantic expects the data to be dictionay but in our case we are using ORM 
    class Config():
        orm_mode = True
