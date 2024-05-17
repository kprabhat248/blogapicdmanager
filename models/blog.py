from pydantic import BaseModel

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