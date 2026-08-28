"""
Configuration management using Pydantic Settings.
Author: Vaibhav Shukla
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Literal


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

    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    # Feature flags
    enable_source_citations: bool = True
    enable_dm_support: bool = True
    max_question_length: int = 500

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def validate_required_keys(self) -> list[str]:
        """Return list of missing required API keys."""
        missing = []
        if not self.openai_api_key:
            missing.append("OPENAI_API_KEY")
        if not self.pinecone_api_key:
            missing.append("PINECONE_API_KEY")
        if not self.slack_bot_token:
            missing.append("SLACK_BOT_TOKEN")
        if not self.slack_app_token:
            missing.append("SLACK_APP_TOKEN")
        if not self.slack_signing_secret:
            missing.append("SLACK_SIGNING_SECRET")
        return missing


@lru_cache()
def get_settings() -> Settings:
    return Settings()
