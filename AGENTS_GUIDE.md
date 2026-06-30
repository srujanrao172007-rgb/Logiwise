# LogiWise — Complete Agent Guide

> Hand this document to any AI coding agent to continue development with full context.

---

## 1. Project Overview

LogiWise is a logistics AI agent built with **Google ADK (Agent Development Kit) v2.x**. It combines shipment tracking, warehouse operations, order management, inventory control, demand forecasting, and profit analysis into a single conversational multi-agent workflow.

**Tech Stack:**
- Python 3.11+, google-adk, litellm, python-dotenv
- LLM Backend: NVIDIA (default: `nvidia/nemotron-4-340b-instruct`)
- Also supports: OpenRouter, Gemini
- Runs as: ADK web server at `localhost:18081`

---

## 2. Project Structure

```
logiwise/
├── app/
│   ├── __init__.py           # Exports `app` object
│   ├── agent.py              # Main agent: Workflow + 3 sub-agents + security nodes
│   ├── tools.py              # 22 mock logistics tools + data
│   ├── forecasting.py        # Demand forecasting engine (moving avg, seasonal, safety stock)
│   ├── config.py             # Multi-backend config (NVIDIA/OpenRouter/Gemini)
│   ├── mcp_server.py         # Deprecated MCP server (not used)
│   └── agent_runtime_app.py  # Agent Runtime entry point
├── .env                      # API keys + model selection
├── .env.example              # Template for new users
├── pyproject.toml            # Dependencies
├── Makefile                  # setup/install/run/test targets
├── FEATURES.md               # Full feature reference with test queries
├── README.md                 # Project documentation
├── DEMO.md                   # Demo script
├── submission_writeup.md     # Submission write-up
├── video_script.md           # 5-min video script with timestamps
├── architecture.png          # Architecture diagram
├── workflow.png              # Workflow diagram
├── thumbnail.png             # Hero/thumbnail image
└── tests/
    ├── unit/
    │   ├── test_dummy.py
    │   └── test_tools.py
    └── integration/
        ├── test_agent.py
        └── test_agent_runtime_app.py
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
     │                          Tools: list_orders, get_order_details, create_order,
     │                          get_shipment_status, predict_delay, notify_customer,
     │                          prioritize_orders, push_urgent_orders,
     │                          calculate_order_margins, minimize_losses
     │
     ├── warehouse keywords ──► WarehouseOps (LlmAgent)
     │                          Tools: list_all_products, get_inventory_level,
     │                          suggest_restock, restock_product, add_product
     │
     └── intelligence keywords ─► InventoryIntelligence (LlmAgent)
                                  Tools: forecast_demand, analyze_customer_demand,
                                  get_reorder_recommendations, auto_replenish,
                                  confirm_replenish, reject_replenish,
                                  suggest_partnerships, search_company_trends,
                                  customer_360
     │
     ▼
security_checkpoint (PII redaction, injection detection, rate limiting, replenishment detection)
     │
     ├── approved ──► final_output
     ├── review   ──► human_approval (RequestInput interrupt with replenishment details)
     │                   ├── approve ──► final_output
     │                   └── deny   ──► blocked_output
     └── blocked  ──► blocked_output
```

### classify_intent Keyword Routing

Located in `app/agent.py` at `classify_intent` function.

- **Shipment keywords:** track, shipment, delivery, delay, carrier, shipping, transit, order, orders, placed, create, new order, add order, deliver, priority, prioritize, rush, urgent, margin, profit, loss, billing, cost
- **Warehouse keywords:** inventory, stock, warehouse, restock, pick, pack, sku, products, product
- **Intelligence keywords:** forecast, replenish, replenishment, reorder, partnership, partner, trend, market, intelligence, growth, demand, projection, seasonal, auto, 360, customer view

Scoring is additive: each keyword adds 1 point. Intelligence takes priority if its score >= both others. Warehouse takes priority over shipment if its score is higher. Ties go to shipment.

---

## 4. Code Files — What Each Contains

### `app/agent.py`

| Section | Lines | Description |
|---------|-------|-------------|
| Imports | 1-14 | ADK imports, config, tools |
| Model setup | 16-23 | Selects LiteLlm (NVIDIA/OpenRouter) or Gemini |
| ShipmentTracker | 54-76 | LlmAgent with 10 order/shipment/margin/priority tools |
| WarehouseOps | 78-94 | LlmAgent with 5 inventory/restock/add tools |
| InventoryIntelligence | 96-120 | LlmAgent with 9 forecasting/replenishment/partnership tools |
| classify_intent | 124-146 | Keyword scoring + 3-route routing node |
| security_checkpoint | 149-208 | PII regex, injection keywords, rate limiting, replenishment detection |
| human_approval | 211-259 | RequestInput interrupt with detailed replenishment proposals |
| final_output | 262-275 | Formats final response with approval results |
| blocked_output | 278-288 | Security-blocked response |
| Workflow edges | 292-309 | Directed graph connecting all nodes |
| App export | 311-314 | `App(root_agent=root_agent, name="app")` |

**Important:** The App is exported as `app` via `__init__.py`. The root_agent is a `Workflow` object, not a simple Agent.

### `app/tools.py`

Contains **22 function tools** + mock data:

#### Order & Shipment Tools
| Function | Description | Key Behavior |
|----------|-------------|--------------|
| `list_orders(customer_id)` | List all orders, optional filter by CUSTxxx | Returns human-readable formatted string |
| `get_order_details(order_id)` | Full order with items, status, tracking | ORD-xxxx format |
| `create_order(customer_name, items_str)` | Create order with auto-SKU resolution | Accepts "ProductName:qty" format. Auto-creates missing customers and products. |
| `get_shipment_status(tracking_number)` | Location, carrier, ETA, delay reason | TRKxxxxx format |
| `predict_delay(tracking_number, location)` | Delay prediction based on location | Random + deterministic logic |
| `notify_customer(customer_id, message, channel)` | Send email/SMS notification | email or sms channel |
| `prioritize_orders(status_filter)` | Rank orders by urgency score | CRITICAL/URGENT/PRIORITY/STANDARD labels |
| `push_urgent_orders()` | Flag CRITICAL/URGENT with SLA action plan | Includes recommended actions |
| `calculate_order_margins(order_id)` | Full P&L: revenue, COGS, shipping, handling, storage | Per-item breakdown |
| `minimize_losses(order_id)` | Cost-saving recommendations | Carrier swap, bundling, pricing tips |

#### Warehouse Tools
| Function | Description | Key Behavior |
|----------|-------------|--------------|
| `list_all_products()` | Full inventory table with stock alerts | Returns formatted list |
| `get_inventory_level(sku)` | Quantity, threshold, restock flag | Accepts SKU or product name via `_find_sku` |
| `suggest_restock(sku)` | Velocity-based restock recommendation | high=3x, medium=2x, low=1x multiplier |
| `restock_product(name_or_sku, quantity)` | Add stock by name or SKU | Uses `_find_sku` for name resolution |
| `add_product(name, quantity, min_threshold, velocity)` | New product with auto-SKU | Category detection from name |

#### Intelligence Tools
| Function | Description | Key Behavior |
|----------|-------------|--------------|
| `forecast_demand(sku, days)` | Daily demand + safety stock + reorder point | Uses moving avg + seasonal multipliers |
| `analyze_customer_demand(customer_id)` | Growth trends, category analysis per customer | Growing/stable/declining detection |
| `get_reorder_recommendations()` | Scan all products for restock needs | Uses forecasting engine |
| `auto_replenish(sku)` | Propose replenishment (human approval required) | Creates PENDING_REPLENISHMENTS entry |
| `confirm_replenish(sku)` | Execute approved replenishment | Calls restock_product internally |
| `reject_replenish(sku, reason)` | Cancel pending replenishment | Logs rejection reason |
| `suggest_partnerships()` | Ranked partner recommendations | Algorithm: Growth(40%) + Frequency(30%) + Diversity(20%) + Recency(10%) |
| `search_company_trends(query)` | Market insights per industry | Industry-specific trend descriptions |
| `customer_360(customer_id)` | Unified profile: orders, P&L, partnership score | Full financial breakdown |

#### Mock Data
- **19 inventory items** across 4 categories (ELEC, WEAR, PACK, FAB)
- **12 customers** with tier (bronze/silver/gold/platinum) and industry
- **23 orders** spanning March-June 2026
- **8 shipments** with various carriers
- **8 suppliers** with lead times and ratings
- **19 product cost entries** with cost/sell price and weight
- **8 shipping rate entries** with base + per-kg pricing

#### Auto-SKU System
- `_detect_category(name)` — maps keywords to categories: elec→ELEC, fab→FAB, pack→PACK, wear→WEAR, etc.
- `_next_sku(category)` — finds max number in existing SKU-CAT-xxx and increments
- `_find_sku(name_or_sku)` — case-insensitive partial name match, returns SKU
- Example: "Silk Thread" → keyword "silk" → category FAB → SKU-FAB-006

### `app/forecasting.py`

| Function | Description |
|----------|-------------|
| `compute_moving_avg(order_history, sku, window_months)` | 3-month weighted moving average |
| `forecast_daily_demand(order_history, sku)` | Monthly base x seasonal / 30 |
| `calculate_safety_stock(daily_demand, lead_time, z_score)` | Z=1.65 (95% service level) x std dev x sqrt(lead time) |
| `calculate_reorder_qty(sku, current_qty, order_history)` | Full reorder decision with safety stock + lead time |

**Seasonal Factors** by category/month — e.g., FAB peaks in Nov-Dec (festival/wedding season), ELEC peaks in Nov-Dec (holiday).

### `app/config.py`

| Field | Env Var | Default |
|-------|---------|---------|
| `model_backend` | MODEL_BACKEND | nvidia |
| `gemini_model` | GEMINI_MODEL | gemini-2.0-flash |
| `openrouter_model` | OPENROUTER_MODEL | openrouter/nvidia/nemotron-3-super-120b-a12b:free |
| `nvidia_model` | NVIDIA_MODEL | nvidia/nemotron-4-340b-instruct |
| `nvidia_api_key` | NVIDIA_API_KEY | (empty) |
| `max_iterations` | (none) | 50 |
| `pii_redaction_enabled` | (none) | True |
| `injection_detection_enabled` | (none) | True |

### `.env`

```
MODEL_BACKEND=nvidia
NVIDIA_MODEL=nvidia/nemotron-4-340b-instruct
NVIDIA_API_KEY=nvapi-...
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

### Replenishment Detection
- Checks `PENDING_REPLENISHMENTS` global dict for pending_approval status
- If found, passes details to human_approval node with full proposal
- Audit log includes `replenishment_pending` field

### Human Approval
- Uses `RequestInput` interrupt pattern
- For replenishment: shows detailed proposal (product, current stock, reorder qty, forecast, safety stock)
- User types "approve", "yes", or "y" to execute all pending replenishments
- User types "deny" or "no" to cancel all pending replenishments
- Executed replenishments call `restock_product` internally

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
uv run adk run app "Forecast demand for SKU-ELEC-004"
uv run adk run app "Show customer 360 for CUST003"
uv run adk run app "Prioritize all orders by urgency"

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
  * Wireless Keyboard x50
  * Corrugated Box M x200
```

### Name-based Lookup Pattern
Tools `restock_product`, `get_inventory_level`, and `_find_sku` accept product names. The agent instructions tell it to use product names directly — never ask the user for SKUs.

### Order Creation Flow
1. Agent calls `create_order(customer_name, items_str)`
2. Items format: `"ProductName:quantity, ProductName:quantity"`
3. Missing products → auto-created in INVENTORY with auto-SKU
4. Missing customers → auto-created in CUSTOMERS with CUSTxxx ID
5. Orders get auto-incremented ORDER-xxxx IDs

### Auto-Replenishment Flow
1. Agent calls `auto_replenish(sku)` → creates PENDING_REPLENISHMENTS entry
2. Security checkpoint detects pending replenishment → routes to human_approval
3. Human approval node shows detailed proposal and pauses for input
4. User types "approve" → `restock_product` called → replenishment executed
5. User types "deny" → proposal rejected with reason

### Sub-agent Instructions
- ShipmentTracker: "Create new orders, look up details, track shipments, predict delays, notify customers, prioritize orders, calculate margins, minimize losses"
- WarehouseOps: "View products, check inventory, restock, add products. Never ask for SKU — use product names."
- InventoryIntelligence: "Forecast demand, analyze customer patterns, get reorder recommendations, auto-replenish, suggest partnerships, search trends, customer 360"

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
CUSTxxx: {name, email, phone, industry, tier (bronze/silver/gold/platinum)}
```

### SUPPLIERS (dict keyed by SUP-xxx)
```
SUP-xxx: {name, lead_time_days, min_order_qty, categories, rating, price_rating}
```

### PRODUCT_COSTS (dict keyed by SKU)
```
SKU-XXX-xxx: {cost, sell, weight_kg}
```

### PENDING_REPLENISHMENTS (dict keyed by SKU)
```
SKU-XXX-xxx: {name, current_qty, reorder_qty, forecast_qty, safety_stock, reorder_point, reason, status, timestamp}
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
- Prioritize orders by urgency and push urgent/rush orders to front (use prioritize_orders)
- Show only urgent orders that need immediate handling (use push_urgent_orders)
- Calculate detailed profit margins for any order including costs (use calculate_order_margins)
- Get recommendations to minimize losses on orders (use minimize_losses)
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

InventoryIntelligence instruction:
```
You are an inventory intelligence and business analyst. You can:
- Forecast demand for any product SKU using historical trends, seasonality, and customer patterns (use forecast_demand)
- Analyze customer buying patterns, growth trends, and partnership potential (use analyze_customer_demand)
- Scan all inventory and recommend which products need reordering with quantity suggestions (use get_reorder_recommendations)
- Auto-calculate and propose replenishment orders that need human approval (use auto_replenish — pass a SKU)
- Execute approved replenishments (use confirm_replenish — pass a SKU)
- Cancel pending replenishments (use reject_replenish — pass SKU and reason)
- Suggest companies for strategic partnership based on order growth, frequency, and category diversity (use suggest_partnerships)
- Research company trends and market insights across our customer database (use search_company_trends)
- Get a complete 360-degree view of any customer with orders, profits, trends, and predictions (use customer_360 - pass CUSTxxx)
IMPORTANT: auto_replenish creates a PENDING proposal that requires human approval.
The user must type 'approve' or 'yes' to execute it.
When user says 'approve', 'yes', or 'confirm', call confirm_replenish with the SKU.
When user says 'reject', 'deny', or 'no', call reject_replenish with the SKU.
```

---

## 12. Forecasting Engine

Located in `app/forecasting.py`:

### Algorithm
1. **Moving Average**: 3-month weighted window of historical order data
2. **Seasonal Multiplier**: Category-specific monthly factors (e.g., FAB peaks in Q4 for festival/wedding season)
3. **Daily Demand**: `(monthly_base * seasonal) / 30`
4. **Safety Stock**: `Z(1.65) * std_dev * sqrt(lead_time)` where std_dev = daily_demand * 0.3
5. **Reorder Point**: `daily_demand * lead_time + safety_stock`
6. **Reorder Qty**: `reorder_point - current_qty + (daily_demand * lead_time * 0.5)`

### Cost & Margin Engine

Located in `app/tools.py`:
- `PRODUCT_COSTS`: per-SKU cost/sell price and weight
- `SHIPPING_RATES`: per-carrier base + per-kg pricing
- `HANDLING_COST`: $2.50 per order
- `STORAGE_COST_PER_UNIT`: $0.05 per unit per week

### Order Prioritization Algorithm

```
Score = Tier(35%) + Urgency(25%) + DelayRisk(20%) + Value(10%) + Recency(10%)
Thresholds: CRITICAL >= 0.55 | URGENT >= 0.45 | PRIORITY >= 0.30 | STANDARD < 0.30
```

### Partnership Score Algorithm

```
Score = Growth(40%) + Frequency(30%) + Diversity(20%) + Recency(10%)
```

---

## 13. Future Enhancements (Not Started)

- Real logistics API integration (FedEx, ShipStation, etc.)
- Persistent database (SQLite/Postgres) instead of in-memory dicts
- Web UI custom frontend (React/Next.js) with red-and-white theme
- Multi-language support
- Analytics dashboard
- Batch order import via CSV
- Live tracking map integration
- Role-based access (admin, warehouse, customer)
- Notification via email/SMS (real SendGrid/Twilio integration)
