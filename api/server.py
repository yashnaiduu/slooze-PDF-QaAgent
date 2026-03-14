import logging

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent.rag_agent import RAGAgent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger("httpx").setLevel(logging.WARNING)

app = FastAPI(
    title="AI PDF RAG Agent",
    description="Upload PDFs, ask questions, and get AI-powered answers using retrieval-augmented generation.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = RAGAgent()


class QueryRequest(BaseModel):
    question: str


class RAGResponseModel(BaseModel):
    answer: str
    sources: list[str]
    num_chunks_used: int


class UploadResponse(BaseModel):
    message: str
    chunks_indexed: int


@app.get("/health")
def health():
    return {"status": "ok", "index_size": agent._retrieval.index_size}


@app.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")

    try:
        count = agent.ingest_bytes(data, filename=file.filename)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    return UploadResponse(message=f"Successfully ingested {file.filename}", chunks_indexed=count)


@app.post("/query", response_model=RAGResponseModel)
def query_document(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    result = agent.query(request.question)
    return RAGResponseModel(
        answer=result.answer,
        sources=result.sources,
        num_chunks_used=result.num_chunks_used,
    )


@app.post("/summarize", response_model=RAGResponseModel)
def summarize_document():
    result = agent.summarize()
    return RAGResponseModel(
        answer=result.answer,
        sources=result.sources,
        num_chunks_used=result.num_chunks_used,
    )


if __name__ == "__main__":
    import uvicorn
    from config.settings import settings

    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
