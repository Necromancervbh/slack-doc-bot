"""
Configuration management using Pydantic Settings.
Author: Vaibhav Shukla
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    embedding_model: str = "text-embedding-3-small"

    # Pinecone
    pinecone_api_key: str = ""
    pinecone_index_name: str = "slack-doc-bot"
    pinecone_environment: str = "us-east-1"

    # Slack
    slack_bot_token: str = ""
    slack_app_token: str = ""
    slack_signing_secret: str = ""

    # RAG Settings
    chunk_size: int = 1000
    chunk_overlap: int = 200
    retrieval_k: int = 4
    docs_directory: str = "docs"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
