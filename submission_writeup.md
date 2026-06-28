# LogiWise — Logistics Agent Submission

## Overview

LogiWise is a conversational AI agent for logistics operations built with Google ADK (Agent Development Kit). It combines shipment tracking, warehouse management, and order processing into a single multi-agent workflow with built-in security guardrails.

## Architecture

LogiWise uses a **Workflow-based multi-agent architecture**:

```
User Input → classify_intent → ShipmentTracker (orders/shipments/tracking)
                             → WarehouseOps (inventory/restock/products)
            → security_checkpoint (PII redaction, injection detection, rate limiting)
            → human_approval (human-in-the-loop for sensitive ops)
            → final_output / blocked_output
```

### Agents
- **ShipmentTracker** — Handles orders, tracking, delay prediction, customer notifications
- **WarehouseOps** — Manages inventory, restocking, product additions

### Security Layer
- PII redaction (phone, email, credit card, tracking numbers)
- Prompt injection detection
- Session rate limiting (50 lookups max)
- Human-in-the-loop approval for flagged operations

## Features

| Feature | Tool | Description |
|---------|------|-------------|
| List Orders | `list_orders` | View all orders, filter by customer |
| Order Details | `get_order_details` | Full order info with items and tracking |
| **Create Order** | **`create_order`** | New orders with auto-SKU resolution |
| Track Shipment | `get_shipment_status` | Real-time location, carrier, ETA |
| Predict Delay | `predict_delay` | Delay risk assessment by location |
| Notify Customer | `notify_customer` | Email/SMS shipment updates |
| List Products | `list_all_products` | Full inventory view with stock alerts |
| Check Inventory | `get_inventory_level` | Per-SKU quantity and threshold check |
| Suggest Restock | `suggest_restock` | Velocity-based restock recommendations |
| **Restock Product** | **`restock_product`** | Add stock by product name or SKU |
| **Add Product** | **`add_product`** | New products with auto-generated SKU |

### Key Innovations
- **Auto-generated SKUs** — Category detection from product name (ELEC, FAB, PACK, WEAR, GEN)
- **Name-based lookup** — All tools accept human-readable product names, SKUs resolved internally
- **Auto-customer creation** — New customers created on-the-fly during order placement
- **Auto-product creation** — Missing products auto-added when creating orders

## Technical Stack

- **Framework**: Google ADK 2.x (Workflow, LlmAgent, LiteLlm)
- **LLM Backend**: OpenRouter (auto-router) / Gemini / Ollama
- **Python**: 3.11+
- **Dependencies**: google-adk, litellm, python-dotenv

## Setup

```bash
git clone <repo-url> logiwise
cd logiwise
uv sync
# Configure .env with API key
make run  # Start server at http://localhost:18081
```

## Sample Conversation

> **User:** Show me all pending orders
> **Agent:** ORD-1005 — Acme Corp — PENDING — Wireless Keyboard x25, USB-C Hub x75

> **User:** Check inventory for Cotton Fabric
> **Agent:** SKU-FAB-001 — Cotton Fabric Roll 50m — 200 units (above threshold)

> **User:** Restock Cotton Fabric by 20
> **Agent:** Restocked: 200 → 220 (+20)

> **User:** Add a new product Silk Thread with quantity 200, min threshold 30
> **Agent:** Added new product: SKU-FAB-006 — Silk Thread (qty: 200, min: 30)

> **User:** Create a new order for Rao Corp with items: Cotton Jacket:234, Silk Thread:50
> **Agent:** Order ORD-1006 created. Items: Cotton Jacket x234, Silk Thread x50. Status: PENDING

> **User:** Track shipment TRK10001
> **Agent:** IN_TRANSIT at Memphis Hub, ETA 2026-06-30 via FedEx

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
- Audit logging for all security events

## Submission Assets

- `app/agent.py` — Main agent with Workflow, sub-agents, security nodes
- `app/tools.py` — 11 tools with mock logistics data
- `app/config.py` — Multi-backend configuration
- `README.md` — Project documentation
- `DEMO.md` — Full demo script with 11 scenarios
