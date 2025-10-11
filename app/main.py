import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 白名单url
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/articles/tags/{tag}")
async def get_articles(tag: str):
    return {
        "message": f"输入tag：{tag}",
    }


"""
    blog-together-backend  Copyright (C) 2025  Checkey_01
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.
"""

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)

