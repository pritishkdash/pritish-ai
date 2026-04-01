from fastapi import FastAPI
from pydantic import BaseModel
from app.rag import retrieve, create_vectorstore
from app.llm import generate_answer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS (for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "Backend running"}

@app.post("/chat")
def chat(q: Query):
    context = retrieve(q.question)
    answer = generate_answer(context, q.question)
    return {"answer": answer}

# Refresh embeddings (VERY IMPRESSIVE FEATURE)
@app.get("/refresh")
def refresh():
    create_vectorstore()
    return {"message": "Vector DB updated"}
