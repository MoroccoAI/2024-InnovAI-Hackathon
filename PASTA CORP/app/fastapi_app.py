# fastapi_app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from legal import Chatbot

app = FastAPI()
chatbot = Chatbot() 

class ChatRequest(BaseModel):
    question: str
    speciality: str

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        answer = chatbot.get_answer(request.question, request.speciality)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))