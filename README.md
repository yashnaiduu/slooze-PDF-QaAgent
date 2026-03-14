# AI PDF RAG Agent

An AI-powered agent that reads PDF documents, builds a searchable knowledge base, and answers questions using retrieval-augmented generation.

## Architecture

```
PDF Upload
  → Text Extraction (PyPDF2)
  → Chunking (configurable size/overlap)
  → Embeddings (sentence-transformers)
  → Vector Store (FAISS / Chroma)
  → Retrieval (top-k similarity)
  → LLM Response (OpenAI / Anthropic / Ollama)
```

```
ai-pdf-rag-agent/
├── agent/
│   └── rag_agent.py            # Main RAG pipeline (ingest, query, summarize)
├── tools/
│   ├── pdf_loader.py           # PDF text extraction
│   └── chunker.py              # Configurable text chunking
├── vectorstore/
│   └── vector_store.py         # FAISS & ChromaDB abstraction
├── services/
│   ├── llm_provider.py         # Multi-provider LLM interface
│   ├── embedding_service.py    # Embedding generation
│   └── retrieval_service.py    # Vector search orchestration
├── api/
│   └── server.py               # FastAPI server
├── config/
│   └── settings.py             # Environment-based configuration
└── tests/
    └── test_rag_agent.py
```

## Supported LLM Providers

| Provider | `LLM_PROVIDER` | Required Keys |
|---|---|---|
| OpenAI | `openai` | `OPENAI_API_KEY` |
| Anthropic | `anthropic` | `ANTHROPIC_API_KEY` |
| Ollama | `ollama` | `OLLAMA_BASE_URL` |
| OpenAI-Compatible | `openai_compatible` | `OPENAI_API_KEY`, `OPENAI_BASE_URL` |

## Setup

```bash
# Clone
git clone https://github.com/<your-username>/ai-pdf-rag-agent.git
cd ai-pdf-rag-agent

# Virtual environment
python -m venv venv
source venv/bin/activate

# Install
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your provider keys
```

## Usage

### API Server

```bash
python -m api.server
# Server starts at http://localhost:8000
```

### API Endpoints

**Upload PDF**
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@document.pdf"
```

Response:
```json
{
  "message": "Successfully ingested document.pdf",
  "chunks_indexed": 42
}
```

**Ask a Question**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the main findings of this paper?"}'
```

Response:
```json
{
  "answer": "The paper's main findings include...",
  "sources": ["Chunk (score: 0.923)", "Chunk (score: 0.891)"],
  "num_chunks_used": 5
}
```

**Summarize Document**
```bash
curl -X POST http://localhost:8000/summarize
```

**Health Check**
```bash
curl http://localhost:8000/health
```

### Python SDK

```python
from agent.rag_agent import RAGAgent

agent = RAGAgent()

# Ingest a PDF
agent.ingest_file("research_paper.pdf")

# Ask questions
result = agent.query("What methodology was used?")
print(result.answer)

# Summarize
summary = agent.summarize()
print(summary.answer)
```

### Streamlit UI

```bash
# Ensure requirements are installed
pip install -r requirements.txt

# Run the UI
streamlit run ui/app.py
```

## Configuration

All settings are managed via environment variables or `.env` file. See `.env.example` for the full list.

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `openai` | LLM backend |
| `LLM_MODEL` | `gpt-4o-mini` | Model name |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence-transformers model |
| `CHUNK_SIZE` | `500` | Characters per chunk |
| `CHUNK_OVERLAP` | `50` | Overlap between chunks |
| `VECTOR_STORE_TYPE` | `faiss` | `faiss` or `chroma` |
| `TOP_K` | `5` | Chunks retrieved per query |

## Tests

```bash
python -m pytest tests/ -v
```

## License

MIT
