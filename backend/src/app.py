from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.rag import get_answer_and_docs
from src.qdrant import upload_website_to_collection
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Chat API",
    description="A simple RAG API using FastAPI",
    version="1.0.0"
)

origins = [
    "http://localhost:3000"  # React app running on localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"]
)

class Message(BaseModel):
    message: str   

@app.post("/chat", description="Endpoint to chat with the API")
def chat(message: Message):
    response = get_answer_and_docs(message.message)
    response_content = {
        "question": message.message,
        "answer": response["answer"],
        "documents": [doc.dict() for doc in response["context"]]
    }
    return JSONResponse(content=response_content, status_code=200)

@app.post("/indexing", description="Index a website through this endpoint")
def indexing(url: Message):
    try:
        response = upload_website_to_collection(url.message)
        return JSONResponse(content={"response": response}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)