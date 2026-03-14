# AI PDF RAG Agent

An AI assistant that reads PDF documents and answers questions about them.

---

## Overview

This system processes PDF documents, builds a searchable knowledge base, and performs retrieval-augmented generation. It extracts text, chunks it, and uses vector search to deliver highly relevant answers to user questions based purely on the document contents.

---

## Features

* PDF text extraction
* Semantic document chunking
* Vector database storage
* Retrieval-augmented generation
* Provider-agnostic LLM support

---

## Architecture

PDF Upload
→ Text Extraction
→ Vector Embeddings
→ Search Retrieval
→ LLM Processing
→ Final Answer

---

## Project Structure

```text
agent/          # Main RAG logic
tools/          # PDF extraction and chunking
vectorstore/    # FAISS and Chroma database
services/       # LLM and embedding orchestration
api/            # FastAPI server endpoints
ui/             # Streamlit visual interface
config/         # Environment configuration
```

---

## Setup

1. Clone repository
2. Create virtual environment
3. Install dependencies
4. Add environment variables
5. Run application

---

## Environment Variables

* `OPENAI_API_KEY`
* `LLM_PROVIDER`
* `LLM_MODEL`
* `EMBEDDING_MODEL`

---

## Running the Project

```bash
pip install -r requirements.txt
streamlit run ui/app.py
```

---

## Example Usage

**Upload PDF:** `research_paper.pdf`

**Question:**
"What methodology was used?"

**Answer:**
The methodology used involved a double-blind study with 500 participants over 6 months.

---

## Design Decisions

* clean modular architecture
* provider-agnostic LLM layer
* pluggable vector store backends
* configurable text chunking
