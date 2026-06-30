# LogiWise — Logistics Agent Submission

## Overview

LogiWise is a conversational AI agent for logistics operations built with Google ADK (Agent Development Kit). It combines shipment tracking, warehouse management, order processing, demand forecasting, profit analysis, and strategic intelligence into a single multi-agent workflow with built-in security guardrails.

## Architecture

LogiWise uses a **Workflow-based multi-agent architecture** with 3 specialized sub-agents:

```
User Input → classify_intent → ShipmentTracker (orders/shipments/tracking/margins/prioritization)
                              → WarehouseOps (inventory/restock/products)
                              → InventoryIntelligence (forecasting/replenishment/partnerships/customer 360)
             → security_checkpoint (PII redaction, injection detection, rate limiting, replenishment detection)
             → human_approval (human-in-the-loop for replenishment proposals)
             → final_output / blocked_output
```

### Agents
- **ShipmentTracker** — Orders, tracking, delay prediction, customer notifications, order prioritization, margin analysis, loss minimization
- **WarehouseOps** — Inventory checks, restocking, product additions with auto-generated SKUs
- **InventoryIntelligence** — Demand forecasting, auto-replenishment (with human approval), customer 360, partnership suggestions, market trend analysis

### Security Layer
- PII redaction (phone, email, credit card, tracking numbers, container codes)
- Prompt injection detection
- Session rate limiting (50 lookups max)
- Replenishment proposal detection with detailed human-in-the-loop approval flow

## Features

| Feature | Tool | Description |
|---------|------|-------------|
| List Orders | `list_orders` | View all orders, filter by customer |
| Order Details | `get_order_details` | Full order info with items and tracking |
| Create Order | `create_order` | New orders with auto-SKU resolution + auto-customer creation |
| Track Shipment | `get_shipment_status` | Real-time location, carrier, ETA |
| Predict Delay | `predict_delay` | Delay risk assessment by location |
| Notify Customer | `notify_customer` | Email/SMS shipment updates |
| Prioritize Orders | `prioritize_orders` | Rank orders CRITICAL/URGENT/PRIORITY/STANDARD |
| Push Urgent Orders | `push_urgent_orders` | SLA-based action plan for critical orders |
| Calculate Margins | `calculate_order_margins` | Full P&L: revenue, COGS, shipping, handling, storage |
| Minimize Losses | `minimize_losses` | Cost-saving recommendations (carrier swaps, bundling, etc.) |
| List Products | `list_all_products` | Full inventory view with stock alerts |
| Check Inventory | `get_inventory_level` | Per-SKU quantity and threshold check |
| Suggest Restock | `suggest_restock` | Velocity-based restock recommendations |
| Restock Product | `restock_product` | Add stock by product name or SKU |
| Add Product | `add_product` | New products with auto-generated SKU |
| Forecast Demand | `forecast_demand` | Daily demand, safety stock, reorder point |
| Analyze Demand | `analyze_customer_demand` | Growth trends, category analysis per customer |
| Reorder Recommendations | `get_reorder_recommendations` | Full scan of what needs restocking |
| Auto-Replenish | `auto_replenish` | Proposed replenishment (requires human approval) |
| Confirm Replenish | `confirm_replenish` | Execute approved replenishment |
| Reject Replenish | `reject_replenish` | Cancel pending replenishment |
| Suggest Partnerships | `suggest_partnerships` | Ranked recommendations by growth-weighted algorithm |
| Search Trends | `search_company_trends` | Market insights per industry |
| Customer 360 | `customer_360` | Unified profile: orders, P&L, partnership score, predictions |

### Key Innovations
- **Auto-generated SKUs** — Category detection from product name (ELEC, FAB, PACK, WEAR)
- **Name-based lookup** — All tools accept human-readable product names, SKUs resolved internally
- **Auto-customer creation** — New customers created on-the-fly during order placement
- **Auto-product creation** — Missing products auto-added when creating orders
- **Demand forecasting** — Weighted moving average + seasonal multipliers + safety stock (Z=1.65)
- **Human-in-the-loop replenishment** — Auto-replenishment pauses for user approval with full proposal details
- **Multi-factor order prioritization** — Tier(35%) + Urgency(25%) + DelayRisk(20%) + Value(10%) + Recency(10%)
- **Data-driven partnership scoring** — Growth(40%) + Frequency(30%) + Diversity(20%) + Recency(10%)

## Technical Stack

- **Framework**: Google ADK 2.x (Workflow, LlmAgent, LiteLlm)
- **LLM Backend**: NVIDIA NIM / OpenRouter / Gemini
- **Python**: 3.11+
- **Dependencies**: google-adk, litellm, python-dotenv

## Setup

```bash
git clone <repo-url> logiwise
cd logiwise
uv sync
# Configure .env with API key (see .env.example)
make run  # Start server at http://localhost:18081
```

## Sample Conversation

> **User:** Show me all pending orders
> **Agent:** ORD-1005 — Acme Corp — PENDING — Wireless Keyboard x25, USB-C Hub x75

> **User:** Forecast demand for SKU-ELEC-004
> **Agent:** Bluetooth Speaker — Forecasted Daily Demand: 4.2 units/day, Safety Stock: 10, Reorder Point: 69

> **User:** Calculate margins for ORD-2004
> **Agent:** Net Profit: $1,234.56, Profit Margin: 18.5%

> **User:** Auto-replenish low stock Bluetooth Speakers
> **Agent:** [REPLENISHMENT_PROPOSAL] ... Status: PENDING HUMAN APPROVAL
> **User:** approve
> **Agent:** Replenishment approved and executed: Bluetooth Speaker: +60 units

## Development

```bash
make install   # uv sync
make run       # Start server
make test      # Run pytest
```

## Security

- PII patterns automatically redacted from outputs
- Prompt injection keywords trigger blocked response
- Rate limiting prevents abuse (50 lookups per session)
- Replenishment proposals require explicit human approval
- Audit logging for all security events

## Submission Assets

- `app/agent.py` — Main agent with Workflow, 3 sub-agents, security nodes, human approval
- `app/tools.py` — 22 tools with mock logistics data
- `app/forecasting.py` — Demand forecasting engine
- `app/config.py` — Multi-backend configuration (NVIDIA/OpenRouter/Gemini)
- `FEATURES.md` — Full feature reference with test queries
- `README.md` — Project documentation
- `DEMO.md` — Full demo script
- `submission_writeup.md` — This file
