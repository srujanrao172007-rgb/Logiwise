# LogiWise - Logistics AI Agent

## How to Run

```powershell
$env:PYTHONIOENCODING='utf-8'; & "C:\Users\sanjay\OneDrive\Desktop\adk workspace\logiwise\.venv\Scripts\adk.exe" web "C:\Users\sanjay\OneDrive\Desktop\adk workspace\logiwise\app"
```

Open http://localhost:8000 in browser.

## Features & Test Queries

### 1. Warehouse / Inventory
| Query | What it does |
|---|---|
| `List all products` | Shows all inventory with SKUs and stock levels |
| `Check inventory for SKU-ELEC-004` | Detailed view of one product |
| `Restock Bluetooth Speakers with 20 units` | Adds stock |
| `Add a new product Titanium Widget with quantity 100` | Creates new product with auto-SKU |

### 2. Orders & Tracking
| Query | What it does |
|---|---|
| `Show me orders for FabIndia Textiles` | Lists orders filtered by customer |
| `Show all orders` | All orders |
| `Get details for order ORD-2004` | Full order details |
| `What is the status of shipment TRK20004?` | Shipment tracking |
| `Predict delay for TRK20004 at Shanghai Port` | Delay prediction |
| `Notify CUST003 about shipment delay via email` | Sends notification |

### 3. Margins & Loss Analysis
| Query | What it does |
|---|---|
| `Calculate margins for ORD-2004` | P&L breakdown: revenue, COGS, shipping, handling, storage, net profit |
| `Minimize losses for ORD-1004` | Suggests cost-saving actions (carrier swap, bundling, etc.) |
| `Minimize losses on all orders` | Scans all orders for loss recovery |

### 4. Priority & Urgency
| Query | What it does |
|---|---|
| `Prioritize all orders by urgency` | Ranks orders CRITICAL/URGENT/PRIORITY/STANDARD |
| `Show urgent orders that need priority pushing` | Action plan with SLA for critical orders |

### 5. Intelligence & Forecasting
| Query | What it does |
|---|---|
| `Forecast demand for SKU-ELEC-004` | Daily demand, safety stock, reorder point |
| `Analyze customer demand for all customers` | Growth trends, category analysis, partnership potential |
| `Get reorder recommendations for all products` | Full scan of what needs restocking |

### 6. Auto-Replenishment (Human Approval)
| Step | Query |
|---|---|
| Propose | `Auto-replenish low stock Bluetooth Speakers` |
| Approve | `approve` (after it pauses) |
| Reject | `deny` (after it pauses) |

### 7. Customer 360
| Query | What it does |
|---|---|
| `Show customer 360 for CUST003` | Full profile: orders, P&L, partnership score, predictions |
| `Search company trends for textile` | Market insights per industry |
| `Suggest partnership opportunities` | Ranked by growth-weighted algorithm |

### 8. Order Creation
| Query | What it does |
|---|---|
| `Create an order for Walkarounds Inc with USB-C Hub:50, Packing Tape Roll:100` | Creates order, auto-creates new customers |

## Architecture
- **3 sub-agents**: ShipmentTracker, WarehouseOps, InventoryIntelligence
- **Workflow**: classify_intent -> sub-agent -> security_checkpoint -> (human_approval or final_output)
- **Security**: PII redaction, injection detection, rate limiting
- **Human Approval**: Auto-replenishment pauses for user to type approve/deny
- **Forecasting**: Weighted moving average + seasonal multipliers + safety stock (Z=1.65)
