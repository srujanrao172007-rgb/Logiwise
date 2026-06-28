# LogiWise — AI-Assisted Development Guide

## Project Overview

LogiWise is a logistics agent built with Google ADK (Agent Development Kit). It combines shipment tracking, warehouse operations, order management, and inventory control into a single conversational interface.

## Key Files

| File | Purpose |
|------|---------|
| `app/agent.py` | Main agent — Workflow with sub-agents and security nodes |
| `app/tools.py` | 11 tools: orders, shipments, inventory, restock, notifications |
| `app/config.py` | Backend-agnostic config (Gemini / OpenRouter / Ollama) |
| `app/__init__.py` | Exports `app` from agent.py |

## Architecture

- **Workflow agent** routes requests via `classify_intent` → ShipmentTracker or WarehouseOps → security_checkpoint → human_approval → final_output
- **ShipmentTracker** — orders, tracking, delay prediction, notifications
- **WarehouseOps** — inventory, restock, add products
- **Security checkpoint** — PII redaction, injection detection, rate limiting

## Commands

```bash
make install  # uv sync
make run      # Start ADK web server at localhost:18081
make test     # Run tests
```

## Tool Notes

- `create_order` accepts product names (not SKUs) and auto-resolves them
- `restock_product` and `get_inventory_level` accept product names or SKUs
- `add_product` auto-generates SKU from category detection
- All tools return human-readable formatted text (not raw JSON)
