.PHONY: setup install playground run test

AGENT_DIR = app

setup:
	uv sync
	@echo "Checking Ollama..."
	@ollama --version 2>nul || echo "Install Ollama from https://ollama.com"
	ollama pull gemma2:9b 2>nul || echo "Ollama not installed — run: ollama pull gemma2:9b"

install:
	uv sync

playground:
	uv run adk web $(AGENT_DIR) --host 127.0.0.1 --port 18081 --reload_agents

run:
	uv run adk web $(AGENT_DIR) --host 127.0.0.1 --port 18081

test:
	uv run pytest tests/
