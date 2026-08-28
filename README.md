# DocBot — AI Slack Assistant for Internal Docs

> **Ask your team's Slack bot anything — and get answers from your actual company documents.**

Built by **Vaibhav Shukla**

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-green.svg)](https://langchain.com)
[![Pinecone](https://img.shields.io/badge/Pinecone-Vector_DB-purple.svg)](https://pinecone.io)
[![Slack Bolt](https://img.shields.io/badge/Slack-Bolt_SDK-4A154B.svg)](https://slack.dev/bolt-python)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What is DocBot?

DocBot is a production-ready AI Slack bot that uses **Retrieval-Augmented Generation (RAG)** to answer team questions from your internal documents.

Drop your PDFs, markdown files, text docs, and Word files into the `docs/` folder — DocBot indexes them into **Pinecone** and answers questions in Slack using **GPT-4o**, always citing the source document.

```
Team member: @DocBot what is our vacation policy?

DocBot: Our vacation policy allows 20 days of paid vacation per year,
        accruing at 1.67 days/month. Requests must be submitted 2 weeks
        in advance via the HR portal.

        Sources: sample_handbook.md
```

---

## Architecture

```
Slack Channel
    │
    ▼
Slack Events API (Socket Mode)
    │
    ▼
Slack Bolt App (app/bot.py)
    │
    ▼
LangChain RAG Chain (app/rag_chain.py)
    │
    ├──► Pinecone Vector DB   (semantic retrieval)
    │         ▲
    │    app/ingestor.py
    │    (PDF/MD/TXT/DOCX)
    │
    └──► OpenAI GPT-4o        (answer synthesis)
```

---

## Features

- **Semantic Search** — Pinecone vector similarity finds the most relevant doc sections
- **RAG Pipeline** — LangChain RetrievalQA with source citation
- **Slack Integration** — Responds to `@DocBot` mentions and DMs
- **Multi-format Ingestor** — PDF, TXT, Markdown, DOCX
- **Refresh Command** — `@DocBot refresh` re-indexes docs without restarting
- **Docker Ready** — Single `docker-compose up` to run everything
- **Unit Tested** — pytest coverage for RAG chain and ingestor

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/vaibhavshukl23/slack-doc-bot.git
cd slack-doc-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

| Variable | Where to get it |
|----------|----------------|
| `OPENAI_API_KEY` | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| `PINECONE_API_KEY` | [app.pinecone.io](https://app.pinecone.io) |
| `SLACK_BOT_TOKEN` | Slack App → OAuth & Permissions |
| `SLACK_APP_TOKEN` | Slack App → Basic Information → App-Level Tokens |
| `SLACK_SIGNING_SECRET` | Slack App → Basic Information |

### 4. Add your documents

Copy your internal docs into the `docs/` folder:

```bash
cp /path/to/your/handbook.pdf docs/
cp /path/to/your/faq.md docs/
# Supported: .pdf, .txt, .md, .docx
```

### 5. Ingest documents into Pinecone

```bash
python scripts/ingest_docs.py
```

### 6. Start the bot

```bash
python -m app.bot
```

Or with Docker:

```bash
docker-compose up
```

---

## Slack App Setup

1. Go to [api.slack.com/apps](https://api.slack.com/apps) and create a new app
2. Under **OAuth & Permissions**, add these Bot Token Scopes:
   - `app_mentions:read`
   - `chat:write`
   - `im:history`
   - `im:read`
   - `im:write`
3. Under **Event Subscriptions**, enable and subscribe to:
   - `app_mention`
   - `message.im`
4. Under **Socket Mode**, enable Socket Mode and create an App-Level Token with `connections:write` scope
5. Install the app to your workspace
6. Copy the tokens to your `.env` file

---

## Usage

| Command | Description |
|---------|-------------|
| `@DocBot what is our parental leave policy?` | Ask any question |
| `@DocBot how do I set up my dev environment?` | Get onboarding help |
| `@DocBot refresh` | Re-index all documents |
| `@DocBot help` | Show usage guide |

The bot also works in **Direct Messages** — no `@mention` needed.

---

## Project Structure

```
slack-doc-bot/
├── app/
│   ├── __init__.py
│   ├── bot.py               # Slack Bolt app + event handlers
│   ├── rag_chain.py         # LangChain RAG pipeline
│   ├── ingestor.py          # Document loading + Pinecone upsert
│   └── config.py            # Pydantic settings
├── docs/                    # Your internal documents go here
│   ├── sample_handbook.md
│   ├── sample_faq.txt
│   └── sample_onboarding.md
├── scripts/
│   └── ingest_docs.py       # CLI to ingest documents
├── tests/
│   ├── test_rag_chain.py
│   └── test_ingestor.py
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Configuration

All settings are controlled via environment variables (see `.env.example`):

| Setting | Default | Description |
|---------|---------|-------------|
| `OPENAI_MODEL` | `gpt-4o` | LLM for answer generation |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model |
| `CHUNK_SIZE` | `1000` | Document chunk size in characters |
| `CHUNK_OVERLAP` | `200` | Overlap between chunks |
| `RETRIEVAL_K` | `4` | Number of docs to retrieve per query |

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Bot Framework | Slack Bolt (Python) |
| LLM | OpenAI GPT-4o |
| Embeddings | OpenAI text-embedding-3-small |
| Vector DB | Pinecone |
| RAG Framework | LangChain |
| Config | Pydantic Settings |
| Testing | pytest |
| Deployment | Docker / docker-compose |

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Author

**Vaibhav Shukla**
- GitHub: [@vaibhavshukl23](https://github.com/vaibhavshukl23)
- Email: vaibhavshukl23@gmail.com

---

> Built with LangChain + Pinecone + Slack Bolt
