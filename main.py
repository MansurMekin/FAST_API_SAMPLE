import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    password: str

class Post(BaseModel):
    id: int
    author: str
    text: str

users = {}
posts = {}

@app.post("/register")
async def register(user: User):
    if user.username in users:
        raise HTTPException(status_code=409, detail="Username already exists")
    users[user.username] = user.password
    return {"message": "User created"}

@app.post("/login")
async def login(user: User):
    if user.username not in users or users[user.username] != user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}

@app.post("/create_post")
async def create_post(post: Post, token: str):
    if token not in users.values():
        raise HTTPException(status_code=401, detail="Unauthorized")
    post.id = uuid.uuid4()
    posts[post.id] = post
    return {"message": "Post created", "id": post.id}

@app.get("/posts")
async def get_posts():
    return posts.values()

@app.get("/post/{id}")
async def get_post(id: int):
    if id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return posts[id]

@app.delete("/post/{id}")
async def delete_post(id: int, token: str):
    if token not in users.values():
        raise HTTPException(status_code=401, detail="Unauthorized")
    if id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")
    del posts[id]
    return {"message": "Post deleted"}
