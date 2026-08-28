"""
Slack Bot - Event handlers using Slack Bolt (Socket Mode).
Author: Vaibhav Shukla

Commands:
  @DocBot <question>   - Ask anything about internal docs
  @DocBot refresh      - Re-ingest documents
  @DocBot help         - Show usage guide
"""

import logging
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from app.config import get_settings
from app.rag_chain import get_rag_bot
from app.ingestor import ingest

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

settings = get_settings()

app = App(
    token=settings.slack_bot_token,
    signing_secret=settings.slack_signing_secret,
)

HELP_TEXT = """
Hey! I am DocBot, your AI-powered team assistant.

Ask me anything about your internal docs and I will find the answer!

Usage:
  @DocBot what is our vacation policy?
  @DocBot how do I set up the dev environment?
  @DocBot refresh  (Re-index all documents)
  @DocBot help     (Show this message)

Supported doc formats: .pdf .txt .md .docx
"""


def format_response(answer: str, sources: list) -> str:
    """Format RAG response as a clean Slack message."""
    blocks = [f"DocBot Answer\n\n{answer}"]
    if sources:
        src_list = "\n".join(f"  - {s}" for s in sources)
        blocks.append(f"\nSources:\n{src_list}")
    blocks.append("\nPowered by LangChain + Pinecone + GPT-4o")
    return "\n".join(blocks)


@app.event("app_mention")
def handle_mention(event, say, client):
    """Handle @DocBot mentions in channels."""
    raw_text = event.get("text", "")
    question = re.sub(r"<@[A-Z0-9]+>", "", raw_text).strip()
    thread_ts = event.get("thread_ts") or event.get("ts")
    user_id = event.get("user", "")
    channel = event.get("channel", "")

    logger.info(f"Mention from {user_id} in {channel}: {question[:60]}")

    if not question:
        say(text=HELP_TEXT, thread_ts=thread_ts)
        return

    if question.lower() in ("refresh", "re-index", "reload"):
        say(text="Re-indexing documents... This may take a moment.", thread_ts=thread_ts)
        try:
            ingest()
            get_rag_bot().reset()
            say(text="Documents re-indexed successfully! Ready to answer questions.", thread_ts=thread_ts)
        except Exception as e:
            logger.error(f"Ingestion error: {e}", exc_info=True)
            say(text=f"Re-indexing failed: {e}", thread_ts=thread_ts)
        return

    if question.lower() in ("help", "?", "usage"):
        say(text=HELP_TEXT, thread_ts=thread_ts)
        return

    say(text="Searching our docs...", thread_ts=thread_ts)

    bot = get_rag_bot()
    response = bot.ask(question)
    reply = format_response(response["answer"], response["sources"])
    say(text=reply, thread_ts=thread_ts)


@app.event("message")
def handle_dm(event, say):
    """Handle direct messages to the bot."""
    if event.get("bot_id") or event.get("subtype") or event.get("channel_type") != "im":
        return

    question = event.get("text", "").strip()
    if not question:
        say(text=HELP_TEXT)
        return

    if question.lower() in ("help", "?", "usage"):
        say(text=HELP_TEXT)
        return

    say(text="Searching our docs...")

    bot = get_rag_bot()
    response = bot.ask(question)
    reply = format_response(response["answer"], response["sources"])
    say(text=reply)


@app.error
def custom_error_handler(error, body, logger):
    logger.exception(f"Error: {error}")
    logger.info(f"Request body: {body}")


def main():
    logger.info("Starting DocBot in Socket Mode...")
    handler = SocketModeHandler(app, settings.slack_app_token)
    handler.start()


if __name__ == "__main__":
    main()
