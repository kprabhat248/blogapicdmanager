from fastapi import FastAPI
from routes.blog import blog_root
app=FastAPI()

from routes.entry import entry_root

app.include_router(entry_root)
app.include_router(blog_root)
