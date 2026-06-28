# LogiWise — Logistics Agent

An intelligent logistics agent built with Google ADK (Agent Development Kit) that combines shipment tracking, warehouse operations, order management, and inventory control into a single conversational interface.

## Features

- **Track Shipments** — Look up real-time status, location, carrier, and ETA by tracking number
- **Predict Delays** — Get delay predictions based on location and current conditions
- **Manage Orders** — List all orders, get order details, and create new orders with auto-resolved SKUs
- **Manage Inventory** — Check stock levels, view low-stock alerts, restock products, and add new products with auto-generated SKUs
- **Notify Customers** — Send email/SMS notifications about shipment status changes
- **Security** — PII redaction, injection detection, rate limiting, and human-in-the-loop approval

## Architecture

```
LogiWise (Workflow)
├── classify_intent      — Routes requests to ShipmentTracker or WarehouseOps
├── ShipmentTracker      — Orders, shipments, tracking, notifications
├── WarehouseOps         — Inventory, restock, add products
├── security_checkpoint  — PII redaction, injection detection, rate limiting
├── human_approval       — Human-in-the-loop for sensitive operations
├── final_output         — Formatted response to user
└── blocked_output       — Security-blocked response
```

### Agent Tools

| Tool | Description |
|------|-------------|
| `list_orders` | List all orders, optionally filtered by customer |
| `get_order_details` | Get full details for a specific order |
| `create_order` | Create a new order — auto-resolves SKUs from product names, auto-creates missing products |
| `get_shipment_status` | Look up current status and location by tracking number |
| `predict_delay` | Predict shipment delays based on location |
| `notify_customer` | Send email/SMS notification to a customer |
| `list_all_products` | View all products with SKUs and stock levels |
| `get_inventory_level` | Check inventory quantity for a SKU |
| `suggest_restock` | Get recommended restock quantity based on sales velocity |
| `restock_product` | Add stock to an existing product (accepts name or SKU) |
| `add_product` | Add a new product with auto-generated SKU |

## Getting Started

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) — Python package manager
- [Ollama](https://ollama.com) — Local LLM (free, no rate limits)

### Quick Setup (Recommended)

```bash
# 1. Install Ollama (if not installed)
#    Download from https://ollama.com

# 2. Pull a model
ollama pull gemma2:9b

# 3. Install dependencies and run
make setup   # uv sync + check Ollama
make run     # Start server at http://localhost:18081
```

### Manual Setup

```bash
uv sync
cp .env.example .env   # Edit to choose backend
make run
```

Supported backends (set `MODEL_BACKEND` in `.env`):
- **Ollama** (default) — `MODEL_BACKEND=ollama` — No API key needed. Free, unlimited. Pull model: `ollama pull gemma2:9b`
- **Gemini** — `MODEL_BACKEND=gemini` — Set `GOOGLE_API_KEY`
- **OpenRouter** — `MODEL_BACKEND=openrouter` — Set `OPENROUTER_API_KEY`

Open http://localhost:18081 in your browser.

### Quick Test

```bash
# Using the CLI
uv run adk run app "Show me all pending orders"
uv run adk run app "Check inventory for Cotton Fabric Roll 50m"
uv run adk run app "Create an order for Rao Corp with Cotton Jacket:234"
```

## Example Conversations

**Track a shipment:**
> User: `Where is my shipment TRK10001?`
> Agent: In transit at Memphis Hub, ETA 2026-06-30 via FedEx.

**Check and restock inventory:**
> User: `Check stock for Cotton Fabric`
> Agent: SKU-FAB-001 — Cotton Fabric Roll 50m, qty: 200, needs restock: No
> User: `Restock by 50`
> Agent: Restocked Cotton Fabric Roll 50m: 200 → 250 (+50)

**Create a new order:**
> User: `I have an order of 234 Cotton Jackets for Rao Corp`
> Agent: What items? (e.g. "Cotton Jacket:234")
> User: `Cotton Jacket:234`
> Agent: Order ORD-1006 created for Rao Corp. Items: Cotton Jacket x234. Status: PENDING.

## Project Structure

```
logiwise/
├── app/
│   ├── __init__.py       # App exports
│   ├── agent.py          # Main agent — Workflow, sub-agents, nodes
│   ├── tools.py          # All tools (orders, shipments, inventory)
│   ├── config.py         # Backend-agnostic config (Gemini/OpenRouter/Ollama)
│   ├── mcp_server.py     # MCP server (deprecated — tools are direct)
│   └── agent_runtime_app.py  # Agent Runtime entry point
├── tests/
├── .env                  # API keys and model config
├── pyproject.toml        # Dependencies
├── Makefile              # Install/run/test targets
└── README.md
```

## Development

```bash
make install   # uv sync
make run       # Start server
make test      # Run tests
```

## License

MIT
