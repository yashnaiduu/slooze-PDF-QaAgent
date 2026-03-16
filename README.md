# PDF AI Assistant

Ask questions about any PDF. Get precise, context-grounded answers.

---

## Overview

Upload a PDF and ask questions about its content. The system extracts and indexes the document, retrieves the most relevant sections, and generates accurate answers using an LLM.

It works entirely off the document — no hallucinations from outside knowledge.

# 📄 AI PDF QA Agent

A production-grade, asynchronous AI RAG (Retrieval-Augmented Generation) agent that allows you to upload PDF documents, extract their textual content, and intelligently answer questions based strictly on the uploaded context.

This agent features a robust `FastAPI` backend utilizing FAISS/Chroma vector stores and a clean `Streamlit` chat interface.

## Features

- PDF text extraction
- Semantic chunking
- Vector search (FAISS or Chroma)
- Retrieval-augmented generation (RAG)
- Document summarization
- Provider-agnostic LLM support (OpenAI, Anthropic, Ollama)
- REST API + Streamlit UI

## 🏗 Architecture

- **Frontend:** Streamlit (`ui/app.py`) for uploading PDFs and chatting with document context.
- **Backend:** FastAPI (`api/server.py`) serving the RAG inference engine endpoint.
- **Vector Store:** Configurable in-memory or persisted vector database (FAISS/Chroma) via `vectorstore/`.
- **RAG Engine:** Intelligent text chunking, document ingestion, and semantic retrieval (`agent/`, `tools/`).
- **LLM Engine:** Configurable provider via OpenAI/Anthropic/Ollama SDKs (`services/`).

## Project Structure

```
agent/        # RAG logic: ingestion, querying, summarization
tools/        # PDF loading and text chunking
services/     # LLM providers and embedding models
vectorstore/  # FAISS / Chroma vector store backends
api/          # FastAPI server
ui/           # Streamlit interface
config/       # Settings loaded from environment
tests/        # Test suite
```

## ⚙️ Setup & Installation

1. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your API keys. Copy `.env.example` to `.env` and fill in your LLM provider keys (e.g., Groq/OpenAI base URL):
   ```bash
   cp .env.example .env
   ```

## Environment Variables

Copy `.env.example` to `.env` and fill in the required values:

| Variable | Description |
|---|---|
| `LLM_PROVIDER` | `openai` \| `anthropic` \| `ollama` \| `openai_compatible` |
| `LLM_MODEL` | Model name (e.g. `gpt-4o-mini`) |
| `OPENAI_API_KEY` | Required if using OpenAI |
| `ANTHROPIC_API_KEY` | Required if using Anthropic |
| `OLLAMA_BASE_URL` | Required if using Ollama (default: `http://localhost:11434`) |
| `EMBEDDING_MODEL` | Sentence transformer model (default: `all-MiniLM-L6-v2`) |
| `VECTOR_STORE_TYPE` | `faiss` \| `chroma` |

## 🚀 How to Run

To run the application, simply execute the included orchestrator script. This will start both the FastAPI backend and Streamlit UI simultaneously in the same terminal.

```bash
source venv/bin/activate
python run.py
```

* The backend API will start on `http://localhost:8001`
* The Streamlit UI will open at `http://localhost:8501`

To stop the agent, press `Ctrl+C` in the terminal to gracefully shut down both services.

## Example Usage

1. Upload `research_paper.pdf`
2. Click **Process Document**
3. Ask: *"What methodology was used?"*

**Answer:**
> The methodology involved a double-blind study with 500 participants over 6 months.

---

## Design Decisions

- **Modular by design** — each layer (loading, chunking, embedding, retrieval, generation) is independent and swappable
- **Provider-agnostic LLM** — switch between OpenAI, Anthropic, or a local Ollama model via one env variable
- **Pluggable vector stores** — FAISS for speed, Chroma for persistence
- **Context-only answers** — the LLM is explicitly prompted to answer only from the document, reducing hallucination
