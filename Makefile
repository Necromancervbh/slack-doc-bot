.PHONY: install ingest run test lint clean docker-up docker-down

install:
	pip install -r requirements.txt

ingest:
	python scripts/ingest_docs.py

run:
	python -m app.bot

test:
	pytest tests/ -v --tb=short

lint:
	flake8 app/ --max-line-length=100

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name ".pytest_cache" -exec rm -rf {} +

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down

help:
	@echo "Available commands:"
	@echo "  make install     Install dependencies"
	@echo "  make ingest      Ingest documents into Pinecone"
	@echo "  make run         Start the Slack bot"
	@echo "  make test        Run unit tests"
	@echo "  make lint        Run flake8 linter"
	@echo "  make docker-up   Start with Docker Compose"
	@echo "  make docker-down Stop Docker containers"
