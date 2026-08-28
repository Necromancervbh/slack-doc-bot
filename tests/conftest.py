"""
pytest configuration and shared fixtures.
Author: Vaibhav Shukla
"""

import pytest
from unittest.mock import MagicMock, patch
from langchain.schema import Document


@pytest.fixture
def sample_documents():
    """Return a list of sample LangChain Documents for testing."""
    return [
        Document(
            page_content="Our vacation policy allows 20 days per year.",
            metadata={"source": "docs/handbook.md", "page": 1},
        ),
        Document(
            page_content="Parental leave is 16 weeks for primary caregivers.",
            metadata={"source": "docs/faq.txt", "page": 1},
        ),
        Document(
            page_content="Dev setup: clone repo, pip install -r requirements.txt, docker-compose up.",
            metadata={"source": "docs/onboarding.md", "page": 1},
        ),
    ]


@pytest.fixture
def mock_rag_chain_result():
    """Return a mock RAG chain result dict."""
    return {
        "result": "Our vacation policy allows 20 days of paid leave per year.",
        "source_documents": [
            MagicMock(metadata={"source": "docs/handbook.md"}),
        ],
    }


@pytest.fixture
def mock_settings():
    """Return mock settings object."""
    settings = MagicMock()
    settings.openai_api_key = "sk-test-key"
    settings.openai_model = "gpt-4o"
    settings.embedding_model = "text-embedding-3-small"
    settings.pinecone_api_key = "test-pinecone-key"
    settings.pinecone_index_name = "slack-doc-bot-test"
    settings.retrieval_k = 4
    settings.chunk_size = 1000
    settings.chunk_overlap = 200
    settings.docs_directory = "docs"
    return settings
