from unittest.mock import MagicMock, patch

import numpy as np

from agent.rag_agent import RAGAgent, RAGResponse
from tools.chunker import chunk_text, TextChunk


class TestChunker:
    def test_basic_chunking(self):
        text = "Hello world. " * 100
        chunks = chunk_text(text, chunk_size=100, chunk_overlap=20)
        assert len(chunks) > 1
        assert all(isinstance(c, TextChunk) for c in chunks)

    def test_chunk_overlap_validation(self):
        try:
            chunk_text("test", chunk_size=10, chunk_overlap=15)
            assert False, "Should have raised ValueError"
        except ValueError:
            pass

    def test_empty_text(self):
        chunks = chunk_text("", chunk_size=100, chunk_overlap=10)
        assert chunks == []

    def test_metadata_populated(self):
        chunks = chunk_text("Some text content here.", chunk_size=50, chunk_overlap=5, source="test.pdf")
        assert chunks[0].metadata["source"] == "test.pdf"


class TestRAGAgent:
    def test_query_no_document(self):
        mock_llm = MagicMock()
        agent = RAGAgent.__new__(RAGAgent)
        agent._llm = mock_llm
        agent._retrieval = MagicMock()
        agent._retrieval.index_size = 0
        agent._document_text = ""

        result = agent.query("What is this about?")
        assert "No document" in result.answer
        mock_llm.generate.assert_not_called()

    def test_query_with_context(self):
        mock_llm = MagicMock()
        mock_llm.generate.return_value = "The document discusses AI systems."

        agent = RAGAgent.__new__(RAGAgent)
        agent._llm = mock_llm
        agent._retrieval = MagicMock()
        agent._retrieval.index_size = 5
        agent._retrieval.retrieve.return_value = [
            ("AI systems are transforming industries.", 0.92),
            ("Machine learning is a subset of AI.", 0.85),
        ]
        agent._document_text = "Full document text."

        result = agent.query("What is this about?")
        assert isinstance(result, RAGResponse)
        assert "AI" in result.answer
        assert result.num_chunks_used == 2

    def test_summarize_no_document(self):
        agent = RAGAgent.__new__(RAGAgent)
        agent._llm = MagicMock()
        agent._document_text = ""

        result = agent.summarize()
        assert "No document" in result.answer
