# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-08-29

### Added
- Initial release of DocBot - AI-powered Slack assistant
- LangChain RetrievalQA pipeline with GPT-4o for answer synthesis
- Pinecone vector database integration for semantic document search
- Slack Bolt (Socket Mode) for real-time event handling
- Multi-format document ingestor supporting PDF, TXT, Markdown, DOCX
- `@DocBot <question>` mention handler in channels
- Direct Message (DM) support without @mention required
- `@DocBot refresh` command to re-index documents without restart
- `@DocBot help` command with usage instructions
- CLI ingestion script: `python scripts/ingest_docs.py`
- Source citation in every answer
- Pydantic Settings for type-safe configuration via .env
- Docker and docker-compose support for easy deployment
- Unit tests with pytest for RAG chain and ingestor modules
- Sample internal docs: handbook, FAQ, onboarding guide
- MIT License

[Unreleased]: https://github.com/Necromancervbh/slack-doc-bot/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Necromancervbh/slack-doc-bot/releases/tag/v1.0.0
