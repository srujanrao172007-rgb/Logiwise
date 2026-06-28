# LogiWise — Complete Agent Guide

> Hand this document to any AI coding agent to continue development with full context.

---

## 1. Project Overview

LogiWise is a logistics AI agent built with **Google ADK (Agent Development Kit) v2.x**. It combines shipment tracking, warehouse operations, order management, and inventory control into a single conversational multi-agent workflow.

**Tech Stack:**
- Python 3.11+, google-adk, litellm, python-dotenv
- LLM Backend: OpenRouter (default: `nvidia/nemotron-3-super-120b-a12b:free`)
- Also supports: Gemini, Ollama
- Runs as: ADK web server at `localhost:18081`

---

## 2. Project Structure

```
logiwise/
├── app/
│   ├── __init__.py          # Exports `app` object
│   ├── agent.py             # Main agent: Workflow + sub-agents + nodes
│   ├── tools.py             # 11 mock logistics tools + data
│   ├── config.py            # Backend config (OpenRouter/Gemini)
│   └── mcp_server.py        # Deprecated MCP server (not used)
├── .env                     # API keys + model selection
├── .env.example             # Template for new users
├── pyproject.toml           # Dependencies
├── Makefile                 # setup/install/run/test targets
├── README.md                # Project documentation
├── DEMO.md                  # 11-scenario demo script
├── submission_writeup.md    # Submission write-up
├── video_script.md          # 5-min video script with timestamps
├── architecture.png         # Architecture diagram
├── workflow.png             # Workflow diagram
├── thumbnail.png            # Hero/thumbnail image
└── tests/                   # Unit and integration tests
```

---

## 3. Architecture

```
User Input
     │
     ▼
classify_intent (keyword scoring node)
     │
     ├── shipment keywords ──► ShipmentTracker (LlmAgent)
     │                          Tools: list_orders, get_order_details,
     │                          create_order, get_shipment_status,
     │                          predict_delay, notify_customer
     │
     └── warehouse keywords ──► WarehouseOps (LlmAgent)
                                Tools: list_all_products,
                                get_inventory_level, suggest_restock,
                                restock_product, add_product
     │
     ▼
security_checkpoint (PII redaction, injection detection, rate limiting)
     │
     ├── approved ──► final_output
     ├── review   ──► human_approval (RequestInput interrupt)
     │                   ├── approve ──► final_output
     │                   └── deny   ──► blocked_output
     └── blocked  ──► blocked_output
```

### classify_intent Keyword Routing

Located in `app/agent.py` at `classify_intent` function.

- **Shipment keywords:** track, shipment, delivery, delay, carrier, shipping, transit, order, orders, placed, create, new order, add order, deliver
- **Warehouse keywords:** inventory, stock, warehouse, restock, pick, pack, sku, products, product

Scoring is additive: each keyword in the user's text adds 1 point. Higher score wins. Ties go to shipment.

---

## 4. Code Files — What Each Contains

### `app/agent.py`

| Section | Lines | Description |
|---------|-------|-------------|
| Imports | 1-32 | ADK imports, config, tools |
| Model setup | 16-20 | Selects LiteLlm (OpenRouter) or Gemini |
| ShipmentTracker | 35-47 | LlmAgent with order/shipment/notify tools |
| WarehouseOps | 49-65 | LlmAgent with inventory/restock/add tools |
| classify_intent | 69-86 | Keyword scoring + routing node |
| security_checkpoint | 89-138 | PII regex, injection keywords, rate limiting |
| human_approval | 141-154 | RequestInput interrupt for approve/deny |
| final_output | 157-167 | Formats final response |
| blocked_output | 170-180 | Security-blocked response |
| Workflow edges | 184-199 | Directed graph connecting all nodes |
| App export | 201-204 | `App(root_agent=root_agent, name="app")` |

**Important:** The App is exported as `app` via `__init__.py`. The root_agent is a `Workflow` object, not a simple Agent.

### `app/tools.py`

Contains **11 function tools** + mock data:

| Function | Description | Key Behavior |
|----------|-------------|--------------|
| `list_orders(customer_id)` | List all orders, optional filter by CUSTxxx | Returns human-readable formatted string |
| `get_order_details(order_id)` | Full order with items, status, tracking | ORD-xxxx format |
| `create_order(customer_name, items_str)` | Create order with auto-SKU resolution | Accepts "ProductName:qty" format. Auto-creates missing customers and products. |
| `get_shipment_status(tracking_number)` | Location, carrier, ETA, delay reason | TRKxxxxx format |
| `predict_delay(tracking_number, location)` | Delay prediction based on location | Random + deterministic logic |
| `notify_customer(customer_id, message, channel)` | Send email/SMS notification | email or sms channel |
| `list_all_products()` | Full inventory table with stock alerts | Returns formatted list |
| `get_inventory_level(sku)` | Quantity, threshold, restock flag | Accepts SKU or product name via `_find_sku` |
| `suggest_restock(sku)` | Velocity-based restock recommendation | high=3x, medium=2x, low=1x multiplier |
| `restock_product(name_or_sku, quantity)` | Add stock by name or SKU | Uses `_find_sku` for name resolution |
| `add_product(name, quantity, min_threshold, velocity)` | New product with auto-SKU | Category detection from name |

**Auto-SKU System:**
- `_detect_category(name)` — maps keywords to categories: elec→ELEC, fab→FAB, pack→PACK, wear→WEAR, etc.
- `_next_sku(category)` — finds max number in existing SKU-CAT-xxx and increments
- `_find_sku(name_or_sku)` — case-insensitive partial name match, returns SKU
- Example: "Silk Thread" → keyword "silk" → category FAB → SKU-FAB-006

**Mock Data:** 9 orders, 10 inventory items, 4 shipments, 3 customers. All real Indian fabric company names (FabIndia Textiles) and products.

### `app/config.py`

| Field | Env Var | Default |
|-------|---------|---------|
| `model_backend` | MODEL_BACKEND | openrouter |
| `gemini_model` | GEMINI_MODEL | gemini-2.0-flash |
| `openrouter_model` | OPENROUTER_MODEL | openrouter/nvidia/nemotron-3-super-120b-a12b:free |
| `max_iterations` | (none) | 50 |
| `pii_redaction_enabled` | (none) | True |
| `injection_detection_enabled` | (none) | True |

### `.env`

```
MODEL_BACKEND=openrouter
OPENROUTER_MODEL=openrouter/nvidia/nemotron-3-super-120b-a12b:free
OPENROUTER_API_KEY=sk-or-v1-...
```

---

## 5. Security System

### PII Redaction (regex patterns)
- Tracking numbers: `\d{5,10}` → [TRACKING_REDACTED]
- Container codes: `[A-Z]{2}\d{6,10}` → [CONTAINER_REDACTED]
- Phone numbers: `\d{3}[-.\s]?\d{3}[-.\s]?\d{4}` → [PHONE_REDACTED]
- Emails: standard regex → [EMAIL_REDACTED]
- Credit cards: `\d{4}-\d{4}-\d{4}-\d{4}` → [CC_REDACTED]

### Injection Detection
Keywords: ignore instructions, system prompt, forget your, role play, you are now, override, bypass, admin

### Rate Limiting
- Counter per session: `lookup_count` in `ctx.state`
- Max: 50 lookups (configurable via `config.max_iterations`)
- Exceeding triggers blocked route

### Human Approval
- Uses `RequestInput` interrupt pattern
- User must type "approve", "yes", or "y" to proceed
- Any other input routes to denied/blocked

---

## 6. How to Run

```bash
# Prerequisites
uv sync                      # Install dependencies
# OR
make install

# Run server
uv run adk web app --host 127.0.0.1 --port 18081
# OR
make run

# Test agent (CLI)
uv run adk run app "Show me all pending orders"

# Test via code
uv run python -c "
import asyncio
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types
from app.agent import root_agent

async def test():
    svc = InMemorySessionService()
    runner = Runner(agent=root_agent, app_name='logiwise', session_service=svc)
    session = await svc.create_session(app_name='logiwise', user_id='test')
    content = types.Content(role='user', parts=[types.Part.from_text(text='List all orders')])
    async for event in runner.run_async(user_id='test', session_id=session.id, new_message=content):
        if event.content and event.content.parts:
            print(''.join(p.text for p in event.content.parts if p.text))

asyncio.run(test())
"
```

---

## 7. Key Patterns & Conventions

### Tool Output Format
All tools return **human-readable formatted strings**, not raw JSON. The agent sees plain text. Example:
```
Order: ORD-1001
Customer: Acme Corp
Status: SHIPPED
Items:
  • Wireless Keyboard x50
  • Corrugated Box M x200
```

### Name-based Lookup Pattern
Tools `restock_product`, `get_inventory_level`, and `_find_sku` accept product names. The agent instructions tell it to use product names directly — never ask the user for SKUs.

### Order Creation Flow
1. Agent calls `create_order(customer_name, items_str)`
2. Items format: `"ProductName:quantity, ProductName:quantity"`
3. Missing products → auto-created in INVENTORY with auto-SKU
4. Missing customers → auto-created in CUSTOMERS with CUSTxxx ID
5. Orders get auto-incremented ORDER-xxxx IDs

### Sub-agent Instructions
- ShipmentTracker: "Create new orders, look up details, track shipments, predict delays, notify customers"
- WarehouseOps: "View products, check inventory, restock, add products. Never ask for SKU — use product names."

---

## 8. Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| 429 rate limits | Free API exhausted | Wait 1 min, or switch model in .env |
| Server won't start | Port in use | Kill old process, or change port |
| `'Context' object has no attribute 'session_state'` | Wrong state API | Use `ctx.state`, not `ctx.session_state` |
| MCP subprocess fails on Windows | MCP not supported | Removed — use direct function tools in tools.py |
| Unicode encoding errors in CLI | Windows console | Set `PYTHONIOENCODING=utf-8` |
| `SessionNotFoundError` | Wrong session_service | Use `InMemorySessionService()` with `create_session` |
| App name mismatch | ADK expects "app" | App name is "app", not "logiwise" |

---

## 9. Development Commands

```bash
uv sync                     # Install deps
uv add <package>            # Add dependency
uv run adk web app          # Start server
uv run adk run app "..."    # Test via CLI
uv run python demo.py       # Run full demo
uv run pytest tests/        # Run tests
make install                # uv sync
make run                    # Start server
make test                   # Run tests
```

---

## 10. Mock Data Schema

### ORDERS (list of dicts)
```
order_id, customer (CUSTxxx), items [{"sku": ..., "qty": ...}],
status (pending/processing/shipped/delayed/delivered),
tracking_number (TRKxxxxx or None), date (YYYY-MM-DD)
```

### INVENTORY (dict keyed by SKU)
```
SKU-XXX-xxx: {name, quantity, min_threshold, velocity (high/medium/low)}
```

### SHIPMENTS (dict keyed by tracking_number)
```
TRKxxxxx: {status, location, eta, carrier, delay_reason?}
```

### CUSTOMERS (dict keyed by customer_id)
```
CUSTxxx: {name, email, phone}
```

---

## 11. Sample Agent Instructions

ShipmentTracker instruction:
```
You are a shipment and order tracking specialist. You can:
- List all orders placed (use list_orders)
- Get details of a specific order (use get_order_details)
- Look up shipment status by tracking number (use get_shipment_status)
- Predict delays (use predict_delay)
- Notify customers about status changes (use notify_customer)
- Create new orders (use create_order — pass customer name and items like 'ProductName:qty')
  Items format example: 'Cotton Jacket:234, Silk Fabric Roll 25m:50'
  The SKU is auto-resolved from the product name. Missing products are auto-created.
IMPORTANT: When user says they have an order to deliver items,
ask for the customer name and items list, then call create_order.
```

WarehouseOps instruction:
```
You are a warehouse operations specialist. You can:
- View all products with their SKUs (use list_all_products)
- Check real-time inventory levels by SKU (use get_inventory_level)
- Flag low-stock items and suggest restocking (use suggest_restock)
- Add stock to existing products (use restock_product — accepts name or SKU)
- Add new products with auto-generated SKU (use add_product)
- Coordinate pick/pack workflow prioritization
IMPORTANT: When user gives a product name like 'Cotton', find the SKU
internally using list_all_products first. Do NOT ask the user for SKU.
For restock: accept product name directly, look up the SKU automatically.
```

---

## 12. Future Enhancements (Not Started)

- Real logistics API integration (FedEx, ShipStation, etc.)
- Persistent database (SQLite/Postgres) instead of in-memory dicts
- Web UI custom frontend (React/Next.js) with red-and-white theme
- Multi-language support
- Analytics dashboard
- Batch order import via CSV
- Live tracking map integration
- Role-based access (admin, warehouse, customer)
- Notification via email/SMS (real SendGrid/Twilio integration)
