from fastapi import FastAPI
from enum import Enum
from fastapi import APIRouter
from routers import blog_get
from routers import imagesummary
from routers import llm_video

app=FastAPI()

app.include_router(imagesummary.router)
app.include_router(llm_video.router)

@app.get('/hello')
def index():
    return "Welcome to the home page! Navigate to routers that handle multimodal data for summarization and transcripting."

