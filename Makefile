.PHONY: install playground run test

AGENT_DIR = app

install:
	uv sync

playground:
	uv run adk web $(AGENT_DIR) --host 127.0.0.1 --port 18081 --reload_agents

run:
	uv run adk web $(AGENT_DIR) --host 127.0.0.1 --port 18081

test:
	uv run pytest tests/
