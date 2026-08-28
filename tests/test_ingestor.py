"""
Unit tests for the document ingestor module.
Author: Vaibhav Shukla
"""

import pytest
from unittest.mock import patch
from langchain.schema import Document
from app.ingestor import chunk_documents, load_documents


class TestChunkDocuments:
    """Tests for the chunk_documents() function."""

    def test_chunks_large_document(self):
        """Test that a large document is split into multiple chunks."""
        long_text = "This is a test sentence. " * 200
        docs = [Document(page_content=long_text, metadata={"source": "test.txt"})]

        with patch("app.ingestor.get_settings") as mock_settings:
            mock_settings.return_value.chunk_size = 500
            mock_settings.return_value.chunk_overlap = 50
            chunks = chunk_documents(docs)

        assert len(chunks) > 1

    def test_chunk_preserves_metadata(self):
        """Test that chunk metadata is preserved from source docs."""
        docs = [
            Document(
                page_content="Short document content for testing purposes.",
                metadata={"source": "test.txt", "page": 1},
            )
        ]

        with patch("app.ingestor.get_settings") as mock_settings:
            mock_settings.return_value.chunk_size = 1000
            mock_settings.return_value.chunk_overlap = 100
            chunks = chunk_documents(docs)

        assert all("source" in c.metadata for c in chunks)


class TestLoadDocuments:
    """Tests for the load_documents() function."""

    def test_raises_for_nonexistent_directory(self):
        """Test that FileNotFoundError is raised for missing directories."""
        with pytest.raises(FileNotFoundError):
            load_documents("/nonexistent/path/to/docs")

    def test_returns_empty_for_no_supported_files(self, tmp_path):
        """Test that empty list is returned when no supported files exist."""
        (tmp_path / "file.xyz").write_text("unsupported")
        (tmp_path / "image.png").write_bytes(b"")

        result = load_documents(str(tmp_path))
        assert result == []
