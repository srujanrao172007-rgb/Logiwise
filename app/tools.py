import random
from datetime import datetime

SHIPMENTS = {
    "TRK10001": {"status": "in_transit", "location": "Memphis Hub", "eta": "2026-06-30", "carrier": "FedEx"},
    "TRK10002": {"status": "delayed", "location": "Port of Los Angeles", "eta": "2026-07-02", "carrier": "Maersk", "delay_reason": "port congestion"},
    "TRK10003": {"status": "delivered", "location": "Customer Dock", "eta": "2026-06-27", "carrier": "UPS"},
    "TRK10004": {"status": "processing", "location": "Chicago Warehouse", "eta": "2026-07-01", "carrier": "DHL"},
    "TRK20001": {"status": "in_transit", "location": "Mumbai Port", "eta": "2026-07-05", "carrier": "Maersk"},
    "TRK20002": {"status": "in_transit", "location": "Singapore Hub", "eta": "2026-07-03", "carrier": "DHL"},
    "TRK20003": {"status": "processing", "location": "Ahmedabad Warehouse", "eta": "2026-07-02", "carrier": "FedEx"},
    "TRK20004": {"status": "delayed", "location": "Shanghai Port", "eta": "2026-07-10", "carrier": "Maersk", "delay_reason": "customs inspection"},
}

INVENTORY = {
    "SKU-ELEC-001": {"name": "Wireless Keyboard", "quantity": 342, "min_threshold": 100, "velocity": "high"},
    "SKU-ELEC-002": {"name": "USB-C Hub", "quantity": 28, "min_threshold": 50, "velocity": "high"},
    "SKU-ELEC-003": {"name": "Monitor Stand", "quantity": 15, "min_threshold": 30, "velocity": "medium"},
    "SKU-WEAR-001": {"name": "Anti-static Gloves", "quantity": 500, "min_threshold": 200, "velocity": "low"},
    "SKU-PACK-001": {"name": "Corrugated Box M", "quantity": 1200, "min_threshold": 500, "velocity": "high"},
    "SKU-FAB-001": {"name": "Cotton Fabric Roll 50m", "quantity": 200, "min_threshold": 50, "velocity": "high"},
    "SKU-FAB-002": {"name": "Silk Fabric Roll 25m", "quantity": 80, "min_threshold": 30, "velocity": "medium"},
    "SKU-FAB-003": {"name": "Linen Fabric Roll 40m", "quantity": 150, "min_threshold": 40, "velocity": "medium"},
    "SKU-FAB-004": {"name": "Polyester Blend Roll 60m", "quantity": 12, "min_threshold": 50, "velocity": "high"},
    "SKU-FAB-005": {"name": "Denim Fabric Roll 30m", "quantity": 100, "min_threshold": 25, "velocity": "low"},
}

CUSTOMERS = {
    "CUST001": {"name": "Acme Corp", "email": "orders@acme.com", "phone": "+1-555-0100"},
    "CUST002": {"name": "GlobalTech Inc", "email": "logistics@globaltech.com", "phone": "+1-555-0200"},
    "CUST003": {"name": "FabIndia Textiles", "email": "purchase@fabindia.com", "phone": "+1-555-0300"},
}

ORDERS = [
    {"order_id": "ORD-1001", "customer": "CUST001", "items": [{"sku": "SKU-ELEC-001", "qty": 50}, {"sku": "SKU-PACK-001", "qty": 200}], "status": "shipped", "tracking_number": "TRK10001", "date": "2026-06-25"},
    {"order_id": "ORD-1002", "customer": "CUST002", "items": [{"sku": "SKU-ELEC-002", "qty": 100}], "status": "delayed", "tracking_number": "TRK10002", "date": "2026-06-26"},
    {"order_id": "ORD-1003", "customer": "CUST001", "items": [{"sku": "SKU-ELEC-003", "qty": 30}], "status": "delivered", "tracking_number": "TRK10003", "date": "2026-06-24"},
    {"order_id": "ORD-1004", "customer": "CUST002", "items": [{"sku": "SKU-WEAR-001", "qty": 500}], "status": "processing", "tracking_number": "TRK10004", "date": "2026-06-27"},
    {"order_id": "ORD-1005", "customer": "CUST001", "items": [{"sku": "SKU-ELEC-001", "qty": 25}, {"sku": "SKU-ELEC-002", "qty": 75}], "status": "pending", "tracking_number": None, "date": "2026-06-28"},
    {"order_id": "ORD-2001", "customer": "CUST003", "items": [{"sku": "SKU-FAB-001", "qty": 100}], "status": "shipped", "tracking_number": "TRK20001", "date": "2026-06-27"},
    {"order_id": "ORD-2002", "customer": "CUST003", "items": [{"sku": "SKU-FAB-003", "qty": 60}, {"sku": "SKU-FAB-005", "qty": 40}], "status": "shipped", "tracking_number": "TRK20002", "date": "2026-06-28"},
    {"order_id": "ORD-2003", "customer": "CUST003", "items": [{"sku": "SKU-FAB-002", "qty": 30}], "status": "processing", "tracking_number": "TRK20003", "date": "2026-06-28"},
    {"order_id": "ORD-2004", "customer": "CUST003", "items": [{"sku": "SKU-FAB-004", "qty": 80}], "status": "delayed", "tracking_number": "TRK20004", "date": "2026-06-26"},
]


def _item_name(sku: str) -> str:
    item = INVENTORY.get(sku, {})
    return item.get("name", sku)


def list_orders(customer_id: str = "") -> str:
    """List all orders placed. Optionally filter by customer ID (e.g. CUST001)."""
    orders = ORDERS
    if customer_id:
        orders = [o for o in orders if o["customer"] == customer_id]
    if not orders:
        return "No orders found."
    lines = ["📦 Orders:"]
    for o in orders:
        cname = CUSTOMERS.get(o["customer"], {}).get("name", o["customer"])
        items_str = ", ".join(f"{_item_name(i['sku'])} x{i['qty']}" for i in o["items"])
        tracking = f" (Track: {o['tracking_number']})" if o["tracking_number"] else ""
        lines.append(f"  • {o['order_id']} — {cname} — {o['status'].upper()}{tracking}")
        lines.append(f"    Items: {items_str}")
    return "\n".join(lines)


CUSTOMER_NAME_TO_ID = {v["name"].lower(): k for k, v in CUSTOMERS.items()}


def _find_or_create_customer(name: str) -> str:
    lower = name.strip().lower()
    if lower in CUSTOMER_NAME_TO_ID:
        return CUSTOMER_NAME_TO_ID[lower]
    existing_ids = sorted(CUSTOMERS.keys())
    new_id = f"CUST{int(existing_ids[-1].replace('CUST', '')) + 1:03d}"
    CUSTOMERS[new_id] = {"name": name.strip(), "email": f"orders@{name.strip().replace(' ', '').lower()}.com", "phone": ""}
    CUSTOMER_NAME_TO_ID[name.strip().lower()] = new_id
    return new_id


def _ensure_product(name: str) -> str | None:
    """Find or return None if product doesn't exist."""
    from_inv = _find_sku(name)
    if from_inv:
        return from_inv
    return None


def _next_order_id() -> str:
    existing_nums = [int(o["order_id"].split("-")[1]) for o in ORDERS]
    return f"ORD-{max(existing_nums) + 1:04d}"


_ORDER_COUNTER = 0


def create_order(customer_name: str, items_str: str) -> str:
    """Create a new order with one or more items.
    customer_name: full customer name (e.g. 'Rao Corp')
    items_str: comma-separated list of 'product name:quantity' (e.g. 'Cotton Jacket:234, Silk Fabric Roll 25m:50')
    Missing products are auto-created in inventory. SKUs are auto-resolved.
    """
    global _ORDER_COUNTER
    cid = _find_or_create_customer(customer_name)
    raw_items = [i.strip() for i in items_str.split(",") if i.strip()]
    items = []
    created_products = []
    for entry in raw_items:
        if ":" not in entry:
            return f"Invalid item format '{entry}'. Use 'ProductName:quantity' (e.g. 'Cotton Jacket:234')."
        name_part, qty_part = entry.rsplit(":", 1)
        try:
            qty = int(qty_part.strip())
        except ValueError:
            return f"Invalid quantity '{qty_part}' in item '{entry}'."
        name = name_part.strip()
        sku = _ensure_product(name)
        if not sku:
            sku = name.upper().replace(" ", "-")[:12]
            existing_skus = set(INVENTORY.keys())
            if sku not in existing_skus:
                pass
            INVENTORY[sku] = {"name": name, "quantity": qty, "min_threshold": 10, "velocity": "medium"}
            created_products.append(f"{name} ({sku})")
        items.append({"sku": sku, "qty": qty})
    _ORDER_COUNTER += 1
    order_id = _next_order_id()
    ORDERS.append({
        "order_id": order_id,
        "customer": cid,
        "items": items,
        "status": "pending",
        "tracking_number": None,
        "date": datetime.now().strftime("%Y-%m-%d"),
    })
    cname = CUSTOMERS[cid]["name"]
    items_detail = "\n".join(f"  • {_item_name(i['sku'])} x{i['qty']}" for i in items)
    created_note = f"\n\nNew products created: {', '.join(created_products)}" if created_products else ""
    return (
        f"Order {order_id} created for {cname}.{created_note}\n\n"
        f"Items:\n{items_detail}\n\n"
        f"Status: PENDING"
    )


def get_order_details(order_id: str) -> str:
    """Get full details for a specific order including items, status, and tracking number."""
    order = next((o for o in ORDERS if o["order_id"] == order_id), None)
    if not order:
        return "Order not found."
    cname = CUSTOMERS.get(order["customer"], {}).get("name", order["customer"])
    items_str = "\n".join(f"  • {_item_name(i['sku'])} x{i['qty']}" for i in order["items"])
    tracking = f"Tracking: {order['tracking_number']}" if order["tracking_number"] else "Not yet shipped"
    return (
        f"Order: {order['order_id']}\n"
        f"Customer: {cname}\n"
        f"Status: {order['status'].upper()}\n"
        f"Date: {order['date']}\n"
        f"{tracking}\n"
        f"Items:\n{items_str}"
    )


def get_shipment_status(tracking_number: str) -> str:
    """Look up the current status and location of a shipment by tracking number."""
    s = SHIPMENTS.get(tracking_number, None)
    if not s:
        return f"No shipment found for tracking number {tracking_number}."
    delay = f" — Reason: {s.get('delay_reason', 'N/A')}" if s.get("status") == "delayed" else ""
    return (
        f"Tracking: {tracking_number}\n"
        f"Status: {s['status'].upper()}\n"
        f"Location: {s['location']}\n"
        f"Carrier: {s['carrier']}\n"
        f"ETA: {s['eta']}{delay}"
    )


def predict_delay(tracking_number: str, location: str) -> str:
    """Predict whether a shipment will be delayed based on location and conditions."""
    shipment = SHIPMENTS.get(tracking_number, {})
    delay_chance = random.uniform(0, 1)
    if shipment.get("status") == "delayed":
        predicted = True
        reason = shipment.get("delay_reason", "operational issue")
    elif "port" in location.lower() or "customs" in location.lower():
        predicted = delay_chance > 0.5
        reason = "port or customs processing" if predicted else "no issues expected"
    else:
        predicted = delay_chance > 0.8
        reason = "weather or traffic" if predicted else "on schedule"
    return str({"tracking_number": tracking_number, "delay_predicted": predicted, "reason": reason, "confidence": "high" if predicted else "medium"})


def get_inventory_level(sku: str) -> str:
    """Check current inventory quantity and status for a given SKU. SKU format: e.g. SKU-FAB-001 for Cotton Fabric Roll 50m, SKU-ELEC-002 for USB-C Hub."""
    item = INVENTORY.get(sku, {"name": "unknown", "quantity": 0, "min_threshold": 0, "velocity": "unknown"})
    needs_restock = item["quantity"] < item["min_threshold"]
    return str({"sku": sku, "name": item["name"], "quantity": item["quantity"], "min_threshold": item["min_threshold"], "needs_restock": needs_restock})


def suggest_restock(sku: str) -> str:
    """Suggest a restock quantity for a low-inventory SKU based on sales velocity."""
    item = INVENTORY.get(sku)
    if not item:
        return str({"error": "SKU not found"})
    velocity_multiplier = {"high": 3, "medium": 2, "low": 1}
    weeks = velocity_multiplier.get(item["velocity"], 1)
    suggested = item["min_threshold"] * weeks - item["quantity"]
    suggested = max(suggested, item["min_threshold"])
    return str({"sku": sku, "name": item["name"], "current_quantity": item["quantity"], "suggested_restock_qty": suggested, "velocity": item["velocity"]})


def notify_customer(customer_id: str, message: str, channel: str) -> str:
    """Send a notification to a customer about their shipment. Channel can be 'email' or 'sms'."""
    customer = CUSTOMERS.get(customer_id, {"name": "Unknown"})
    return str({"status": "sent", "customer": customer["name"], "channel": channel, "message": message, "timestamp": datetime.now().isoformat()})


_CATEGORY_MAP = {
    "elec": "ELEC", "electronic": "ELEC", "keyboard": "ELEC", "usb": "ELEC", "monitor": "ELEC",
    "wear": "WEAR", "glove": "WEAR", "safety": "WEAR",
    "pack": "PACK", "box": "PACK", "corrugated": "PACK",
    "fab": "FAB", "fabric": "FAB", "cotton": "FAB", "silk": "FAB", "linen": "FAB", "polyester": "FAB", "denim": "FAB",
}


def _detect_category(name: str) -> str:
    lower = name.lower()
    for keyword, cat in _CATEGORY_MAP.items():
        if keyword in lower:
            return cat
    return "GEN"


def _next_sku(category: str) -> str:
    existing = [k for k in INVENTORY if k.startswith(f"SKU-{category}-")]
    if not existing:
        return f"SKU-{category}-001"
    nums = [int(k.split("-")[-1]) for k in existing]
    return f"SKU-{category}-{max(nums) + 1:03d}"


def _find_sku(name_or_sku: str) -> str | None:
    name_or_sku = name_or_sku.strip()
    if name_or_sku.upper().startswith("SKU-"):
        return name_or_sku if name_or_sku in INVENTORY else None
    lower = name_or_sku.lower()
    for sku, item in INVENTORY.items():
        if lower == item["name"].lower():
            return sku
    for sku, item in INVENTORY.items():
        if lower in item["name"].lower():
            return sku
    return None


def list_all_products() -> str:
    """List all products in inventory with their names and SKUs."""
    lines = ["Inventory:"]
    for sku in sorted(INVENTORY):
        item = INVENTORY[sku]
        flag = " ⚠ LOW" if item["quantity"] < item["min_threshold"] else ""
        lines.append(f"  {sku} — {item['name']} — qty: {item['quantity']}{flag}")
    return "\n".join(lines)


def restock_product(name_or_sku: str, quantity: int) -> str:
    """Add stock to an existing product. Provide the product name or SKU and the quantity to add."""
    sku = _find_sku(name_or_sku)
    if not sku:
        available = "\n".join(f"  {s} — {i['name']}" for s, i in sorted(INVENTORY.items()))
        return f"Product '{name_or_sku}' not found. Available products:\n{available}"
    item = INVENTORY[sku]
    old_qty = item["quantity"]
    item["quantity"] = old_qty + quantity
    return f"Restocked {item['name']} ({sku}): {old_qty} → {item['quantity']} (+{quantity})"


def add_product(name: str, quantity: int, min_threshold: int = 50, velocity: str = "medium") -> str:
    """Add a new product to inventory. SKU is auto-generated. Velocity: high/medium/low."""
    for sku, item in INVENTORY.items():
        if item["name"].lower() == name.lower():
            return f"Product '{name}' already exists as {sku}. Use restock_product to add stock."
    category = _detect_category(name)
    sku = _next_sku(category)
    INVENTORY[sku] = {"name": name, "quantity": quantity, "min_threshold": min_threshold, "velocity": velocity}
    return f"Added new product: {sku} — {name} (qty: {quantity}, min: {min_threshold}, velocity: {velocity})"
