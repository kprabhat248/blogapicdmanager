from fastapi import APIRouter
from models.blog import blogmodel,updateblogmodel
from config.config import blogs_connection
from serializers.serializers import decodeblog,decodeblogs
from bson import ObjectId
import datetime
blog_root=APIRouter()
###post request
@blog_root.post("/new/blog")
def newblog(doc:blogmodel):
    doc=dict(doc)
    currentdate=datetime.date.today()
    doc["date"]=str(currentdate)
    res=blogs_connection.insert_one(doc)
    doc_id=str(res.inserted_id)
    return{
        "status":"ok",
        "message":"blog posted successfully",
        "_id" : doc_id
    }

###get blogs
@blog_root.get("/all/blogs")
def Allblogs():
    res=blogs_connection.find()
    decodedata=decodeblogs(res)
    return {
        "status":"ok",
        "data":decodedata
    }
###get blog
@blog_root.get("/blog/{_id}")
def getblog(_id:str):
    res=blogs_connection.find_one({"_id": ObjectId(_id) })
    decodedt=decodeblog(res)
    return {
        "status":"ok",
        "data":decodedt
    }

###update blog
@blog_root.patch("/update/{_id}")
def update(_id:str,doc:updateblogmodel):
    req=dict(doc.model_dump(exclude_unset=True))
    blogs_connection.find_one_and_update({"_id": ObjectId(_id) },{
        "$set":req})
    return {
        "status":"Ok",
        "message":"Blog updated successfully"
    }
###delete blog
@blog_root.delete("/delete")
def deleteblog(_id:str):
    blogs_connection.find_one_and_delete(
        {
            "_id":ObjectId(_id)
        })
    return{
        "status":"Okay",
        "message":"Blog deleted successfully"
    }
