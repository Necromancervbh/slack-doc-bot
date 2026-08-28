"""
Unit tests for the RAG chain module.
Author: Vaibhav Shukla
"""

import pytest
from unittest.mock import MagicMock
from app.rag_chain import RAGBot, RAGResponse


class TestRAGBot:
    """Tests for the RAGBot class."""

    def test_ask_returns_rag_response(self):
        """Test that ask() returns a properly typed RAGResponse."""
        bot = RAGBot()
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = {
            "result": "Our vacation policy allows 20 days per year.",
            "source_documents": [
                MagicMock(metadata={"source": "docs/sample_handbook.md"}),
            ],
        }
        bot._chain = mock_chain

        response = bot.ask("What is the vacation policy?")

        assert isinstance(response, dict)
        assert "answer" in response
        assert "sources" in response
        assert "vacation" in response["answer"].lower()
        assert "sample_handbook.md" in response["sources"]

    def test_ask_handles_exception_gracefully(self):
        """Test that ask() returns a friendly error on exception."""
        bot = RAGBot()
        mock_chain = MagicMock()
        mock_chain.invoke.side_effect = Exception("Connection timeout")
        bot._chain = mock_chain

        response = bot.ask("What is the leave policy?")

        assert "error" in response["answer"].lower()
        assert response["sources"] == []

    def test_reset_clears_chain(self):
        """Test that reset() sets the chain to None."""
        bot = RAGBot()
        bot._chain = MagicMock()
        bot.reset()
        assert bot._chain is None

    def test_ask_empty_source_docs(self):
        """Test handling when no source documents are returned."""
        bot = RAGBot()
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = {
            "result": "I could not find that in our internal docs.",
            "source_documents": [],
        }
        bot._chain = mock_chain

        response = bot.ask("Who is the CEO?")
        assert response["sources"] == []
        assert len(response["answer"]) > 0
