"""
RAG Chain - Retrieval-Augmented Generation pipeline using LangChain.
Author: Vaibhav Shukla

Flow:
  User question --> Pinecone retrieval --> GPT-4o synthesis --> Answer + sources
"""

import logging
import time
from typing import TypedDict

from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from app.config import get_settings
from app.ingestor import get_vector_store

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a helpful internal team assistant. You answer questions based ONLY on the provided company documents.
If the answer is not in the documents, say: I could not find that in our internal docs. Please check with the team directly.

Always be concise, friendly, and professional. When possible, mention which document the information came from.

Context from internal documents:
{context}

Question: {question}

Answer:"""

QA_PROMPT = PromptTemplate(
    template=SYSTEM_PROMPT,
    input_variables=["context", "question"],
)


class RAGResponse(TypedDict):
    answer: str
    sources: list[str]
    latency_ms: float


def build_rag_chain() -> RetrievalQA:
    """Build and return the LangChain RAG chain."""
    settings = get_settings()

    llm = ChatOpenAI(
        model=settings.openai_model,
        openai_api_key=settings.openai_api_key,
        temperature=0.2,
        streaming=False,
    )

    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": settings.retrieval_k},
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_PROMPT},
    )

    logger.info("RAG chain built successfully")
    return chain


class RAGBot:
    """Wrapper around the RAG chain with lazy loading, latency tracking, and response formatting."""

    def __init__(self):
        self._chain = None
        self.total_queries: int = 0
        self.total_latency_ms: float = 0.0

    def _get_chain(self) -> RetrievalQA:
        if self._chain is None:
            self._chain = build_rag_chain()
        return self._chain

    def ask(self, question: str) -> RAGResponse:
        """Ask a question and get an answer with source citations and latency."""
        settings = get_settings()

        # Truncate overly long questions
        if len(question) > settings.max_question_length:
            question = question[:settings.max_question_length]
            logger.warning("Question truncated to max_question_length")

        logger.info(f"Processing question: {question[:80]}...")
        chain = self._get_chain()

        start = time.monotonic()
        try:
            result = chain.invoke({"query": question})
            latency_ms = round((time.monotonic() - start) * 1000, 2)

            answer = result.get("result", "Sorry, I could not generate an answer.")
            source_docs = result.get("source_documents", [])
            sources = list(
                {
                    doc.metadata.get("source", "Unknown").replace("\\", "/").split("/")[-1]
                    for doc in source_docs
                }
            )

            self.total_queries += 1
            self.total_latency_ms += latency_ms
            logger.info(f"Answer generated in {latency_ms}ms")

            return RAGResponse(answer=answer, sources=sources, latency_ms=latency_ms)

        except Exception as e:
            latency_ms = round((time.monotonic() - start) * 1000, 2)
            logger.error(f"RAG chain error: {e}", exc_info=True)
            return RAGResponse(
                answer="I encountered an error processing your question. Please try again.",
                sources=[],
                latency_ms=latency_ms,
            )

    @property
    def avg_latency_ms(self) -> float:
        """Average query latency in milliseconds."""
        if self.total_queries == 0:
            return 0.0
        return round(self.total_latency_ms / self.total_queries, 2)

    def reset(self):
        """Force rebuild of the chain after re-ingestion."""
        self._chain = None
        logger.info("RAG chain reset.")


_rag_bot = None


def get_rag_bot() -> RAGBot:
    global _rag_bot
    if _rag_bot is None:
        _rag_bot = RAGBot()
    return _rag_bot
