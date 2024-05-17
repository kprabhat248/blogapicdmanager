from pydantic import BaseModel, EmailStr

class blogmodel(BaseModel):
    title:str
    subtitle:str
    content:str
    author:str
    tags:list

class updateblogmodel(BaseModel):
    title:str = None
    subtitle:str=None
    content:str=None
    author:str=None
    tags:list=None

class UserRegisterModel(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLoginModel(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str