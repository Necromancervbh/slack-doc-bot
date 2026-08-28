#!/usr/bin/env python
"""
CLI script to ingest documents into Pinecone.
Author: Vaibhav Shukla

Usage:
    python scripts/ingest_docs.py
    python scripts/ingest_docs.py --docs-dir /path/to/docs
"""

import sys
import argparse
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.ingestor import ingest

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Ingest documents into Pinecone for the Slack Doc Bot."
    )
    parser.add_argument(
        "--docs-dir",
        default="docs",
        help="Path to the directory containing documents (default: docs/)",
    )
    args = parser.parse_args()

    logger.info(f"Starting document ingestion from: {args.docs_dir}")

    try:
        ingest(docs_dir=args.docs_dir)
        logger.info("All documents ingested successfully!")
        logger.info("Start the bot with: python -m app.bot")
    except FileNotFoundError as e:
        logger.error(f"Directory not found: {e}")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Ingestion error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
