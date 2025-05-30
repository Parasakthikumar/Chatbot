from fastapi import APIRouter, Request
from pydantic import BaseModel
from rag.query_handler import handle_query

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

@router.post("/chat")
async def chat(req: ChatRequest):
    return await handle_query(req.question)
