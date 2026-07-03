from fastapi import FastAPI
from pydantic import BaseModel
from app.chat_logic import generate_response

app = FastAPI()


class ChatRequest(BaseModel):
    messages: list


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    return generate_response(request.messages)