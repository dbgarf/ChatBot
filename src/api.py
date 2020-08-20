from fastapi import FastAPI

from src.chatbot import ChatBot

app = FastAPI()

@app.get("/")
async def chatbot_root(message):
    cb = ChatBot()
    result = cb.handle_message(message)
    return result

