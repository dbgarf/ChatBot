from fastapi import FastAPI

from src.chatbot import ChatBot, UndefinedCommandError

app = FastAPI()

@app.get("/")
async def chatbot_root(message):
    cb = ChatBot()
    try:
        result = cb.handle_message(message)
        return result
    except UndefinedCommandError:
        return "undefined command. available commands: %s" % cb.available_commands()

