.PHONY: setup install playground run test

AGENT_DIR = app

setup:
	uv sync
	@echo "Configure your .env with an API key (see .env.example)"

install:
	uv sync

playground:
	uv run adk web $(AGENT_DIR) --host 127.0.0.1 --port 18081 --reload_agents

run:
	uv run adk web $(AGENT_DIR) --host 127.0.0.1 --port 18081

test:
	uv run pytest tests/
