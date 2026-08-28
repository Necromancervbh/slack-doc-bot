"""
Document Ingestor - loads, chunks, and upserts docs into Pinecone.
Author: Vaibhav Shukla
"""

import logging
from pathlib import Path
from typing import List

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    UnstructuredMarkdownLoader,
    Docx2txtLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain.schema import Document

from app.config import get_settings

logger = logging.getLogger(__name__)

LOADER_MAP = {
    ".txt": TextLoader,
    ".md": UnstructuredMarkdownLoader,
    ".pdf": PyPDFLoader,
    ".docx": Docx2txtLoader,
}


def load_documents(directory: str) -> List[Document]:
    """Recursively load all supported documents from a directory."""
    docs: List[Document] = []
    path = Path(directory)

    if not path.exists():
        raise FileNotFoundError(f"Documents directory not found: {directory}")

    for file_path in path.rglob("*"):
        suffix = file_path.suffix.lower()
        if suffix not in LOADER_MAP:
            continue
        try:
            loader_cls = LOADER_MAP[suffix]
            loader = loader_cls(str(file_path))
            loaded = loader.load()
            for doc in loaded:
                doc.metadata["source"] = str(file_path)
            docs.extend(loaded)
            logger.info(f"Loaded {len(loaded)} chunks from {file_path.name}")
        except Exception as e:
            logger.warning(f"Failed to load {file_path}: {e}")

    logger.info(f"Total documents loaded: {len(docs)}")
    return docs


def chunk_documents(docs: List[Document]) -> List[Document]:
    """Split documents into smaller overlapping chunks."""
    settings = get_settings()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    logger.info(f"Split into {len(chunks)} chunks")
    return chunks


def get_or_create_index(pc: Pinecone, index_name: str, dimension: int = 1536) -> None:
    """Create Pinecone index if it does not already exist."""
    existing = [idx.name for idx in pc.list_indexes()]
    if index_name not in existing:
        logger.info(f"Creating Pinecone index: {index_name}")
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        logger.info(f"Index created: {index_name}")
    else:
        logger.info(f"Index already exists: {index_name}")


def ingest(docs_dir: str = None) -> PineconeVectorStore:
    """Full ingestion pipeline: load, chunk, embed, upsert to Pinecone."""
    settings = get_settings()
    directory = docs_dir or settings.docs_directory

    logger.info(f"Starting ingestion from: {directory}")
    raw_docs = load_documents(directory)
    if not raw_docs:
        raise ValueError(f"No supported documents found in: {directory}")

    chunks = chunk_documents(raw_docs)

    embeddings = OpenAIEmbeddings(
        model=settings.embedding_model,
        openai_api_key=settings.openai_api_key,
    )

    pc = Pinecone(api_key=settings.pinecone_api_key)
    get_or_create_index(pc, settings.pinecone_index_name, dimension=1536)

    logger.info(f"Upserting {len(chunks)} chunks into Pinecone...")
    vector_store = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=settings.pinecone_index_name,
    )
    logger.info("Ingestion complete")
    return vector_store


def get_vector_store() -> PineconeVectorStore:
    """Connect to existing Pinecone vector store."""
    settings = get_settings()
    embeddings = OpenAIEmbeddings(
        model=settings.embedding_model,
        openai_api_key=settings.openai_api_key,
    )
    return PineconeVectorStore(
        index_name=settings.pinecone_index_name,
        embedding=embeddings,
        pinecone_api_key=settings.pinecone_api_key,
    )
