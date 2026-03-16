# 📄 AI PDF QA Agent

A production-grade RAG (Retrieval-Augmented Generation) agent — upload any PDF, ask questions, and get precise, context-grounded answers.

## 🏗 Architecture

- **Frontend:** Streamlit chat interface (`ui/app.py`)
- **Backend:** FastAPI RAG engine (`api/server.py`)
- **Vector Store:** FAISS for fast semantic search (`vectorstore/`)
- **RAG Pipeline:** PDF loading → chunking → embedding → retrieval → LLM generation
- **LLM:** Groq / OpenAI-compatible APIs (`services/`)

## ⚙️ Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in GROQ_API_KEY
```

## 🚀 Run

```bash
python run.py
```

- Backend API: `http://localhost:8001`
- Streamlit UI: `http://localhost:8501`

Press `Ctrl+C` to shut down both services.

## Environment Variables

| Variable | Description |
|---|---|
| `LLM_PROVIDER` | `openai_compatible` (default for Groq) |
| `LLM_MODEL` | e.g. `llama-3.3-70b-versatile` |
| `GROQ_API_KEY` | Your Groq API key |
| `EMBEDDING_MODEL` | Default: `all-MiniLM-L6-v2` |
| `VECTOR_STORE_TYPE` | `faiss` |

## Example Usage

1. Upload `research_paper.pdf`
2. Click **Process Document**
3. Ask: *"What methodology was used?"*

> The methodology involved a double-blind study with 500 participants over 6 months.

## Design Decisions

- **Modular** — loading, chunking, embedding, retrieval, and generation are independent layers
- **Provider-agnostic** — swap LLMs with a single env variable
- **Context-only answers** — the LLM is prompted to answer strictly from the document
- **Lightweight** — runs entirely in-memory with FAISS, no external DB required
