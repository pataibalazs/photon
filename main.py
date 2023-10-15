from fastapi import FastAPI
from utils import callGPT

app = FastAPI()


@app.get("/")
async def initial():
    return {"message": "Welcome!"}

@app.get("/prompt")
async def generatePrompts(text: str):
    return callGPT(text)