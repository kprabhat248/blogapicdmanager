from fastapi import FastAPI, Depends, HTTPException, APIRouter
from models.blog import blogmodel, updateblogmodel
from models.blog import UserRegisterModel, UserLoginModel, Token
from config.config import blogs_connection, users_connection
from serializers.serializers import decodeblog, decodeblogs
from bson import ObjectId
import datetime
import httpx
from config.jwt import create_access_token, get_password_hash, verify_password, verify_token, oauth2_scheme

app = FastAPI()
blog_root = APIRouter()

### User registration
@blog_root.post("/register", response_model=Token)
async def register(user: UserRegisterModel):
    user_data = {
        "username": user.username,
        "email": user.email,
        "hashed_password": get_password_hash(user.password),
    }

    existing_user = users_connection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    users_connection.insert_one(user_data)
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

### User login
@blog_root.post("/login", response_model=Token)
async def login(user: UserLoginModel):
    db_user = users_connection.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

### Dependency to get the current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    user = users_connection.find_one({"username": username})
    if user is None:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return {"username": username}

### post request
@blog_root.post("/new/blog")
async def newblog(doc: blogmodel, current_user: dict = Depends(get_current_user)):
    doc = dict(doc)
    currentdate = datetime.date.today()
    doc["date"] = str(currentdate)
    res = blogs_connection.insert_one(doc)
    doc_id = str(res.inserted_id)
    return {
        "status": "ok",
        "message": "blog posted successfully",
        "_id": doc_id
    }

### get blogs
@blog_root.get("/all/blogs")
async def Allblogs(current_user: dict = Depends(get_current_user)):
    res = blogs_connection.find()
    decodedata = decodeblogs(res)
    return {
        "status": "ok",
        "data": decodedata
    }

### get blog
@blog_root.get("/blog/{_id}")
async def getblog(_id: str, current_user: dict = Depends(get_current_user)):
    res = blogs_connection.find_one({"_id": ObjectId(_id)})
    if res is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    decodedt = decodeblog(res)
    return {
        "status": "ok",
        "data": decodedt
    }

### update blog
@blog_root.patch("/update/{_id}")
async def update(_id: str, doc: updateblogmodel, current_user: dict = Depends(get_current_user)):
    req = dict(doc.model_dump(exclude_unset=True))
    blogs_connection.find_one_and_update({"_id": ObjectId(_id)}, {
        "$set": req})
    return {
        "status": "Ok",
        "message": "Blog updated successfully"
    }

### delete blog
@blog_root.delete("/delete")
async def deleteblog(_id: str, current_user: dict = Depends(get_current_user)):
    blogs_connection.find_one_and_delete(
        {
            "_id": ObjectId(_id)
        })
    return {
        "status": "Okay",
        "message": "Blog deleted successfully"
    }

### HTTPX example for an external API call
@blog_root.get("/external/api")
async def external_api(current_user: dict = Depends(get_current_user)):
    url = "https://api.example.com/data"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return {
                "status": "ok",
                "data": response.json()
            }
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching data from external API")

app.include_router(blog_root)
