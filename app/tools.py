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
    "TRK30001": {"status": "in_transit", "location": "Delhi Hub", "eta": "2026-07-01", "carrier": "BlueDart"},
    "TRK30002": {"status": "delivered", "location": "Customer Dock", "eta": "2026-06-29", "carrier": "Delhivery"},
    "TRK30003": {"status": "delayed", "location": "Chennai Port", "eta": "2026-07-08", "carrier": "Maersk", "delay_reason": "weather disruption"},
    "TRK30004": {"status": "processing", "location": "Bangalore Warehouse", "eta": "2026-07-04", "carrier": "EcomExpress"},
}

INVENTORY = {
    "SKU-ELEC-001": {"name": "Wireless Keyboard", "quantity": 342, "min_threshold": 100, "velocity": "high"},
    "SKU-ELEC-002": {"name": "USB-C Hub", "quantity": 28, "min_threshold": 50, "velocity": "high"},
    "SKU-ELEC-003": {"name": "Monitor Stand", "quantity": 15, "min_threshold": 30, "velocity": "medium"},
    "SKU-ELEC-004": {"name": "Bluetooth Speaker", "quantity": 0, "min_threshold": 40, "velocity": "high"},
    "SKU-ELEC-005": {"name": "Laptop Charger 65W", "quantity": 8, "min_threshold": 60, "velocity": "high"},
    "SKU-WEAR-001": {"name": "Anti-static Gloves", "quantity": 500, "min_threshold": 200, "velocity": "low"},
    "SKU-WEAR-002": {"name": "Safety Goggles", "quantity": 45, "min_threshold": 80, "velocity": "medium"},
    "SKU-WEAR-003": {"name": "Industrial Apron", "quantity": 120, "min_threshold": 60, "velocity": "medium"},
    "SKU-PACK-001": {"name": "Corrugated Box M", "quantity": 1200, "min_threshold": 500, "velocity": "high"},
    "SKU-PACK-002": {"name": "Packing Tape Roll", "quantity": 60, "min_threshold": 100, "velocity": "high"},
    "SKU-PACK-003": {"name": "Bubble Wrap Sheet", "quantity": 25, "min_threshold": 80, "velocity": "medium"},
    "SKU-FAB-001": {"name": "Cotton Fabric Roll 50m", "quantity": 200, "min_threshold": 50, "velocity": "high"},
    "SKU-FAB-002": {"name": "Silk Fabric Roll 25m", "quantity": 80, "min_threshold": 30, "velocity": "medium"},
    "SKU-FAB-003": {"name": "Linen Fabric Roll 40m", "quantity": 150, "min_threshold": 40, "velocity": "medium"},
    "SKU-FAB-004": {"name": "Polyester Blend Roll 60m", "quantity": 12, "min_threshold": 50, "velocity": "high"},
    "SKU-FAB-005": {"name": "Denim Fabric Roll 30m", "quantity": 100, "min_threshold": 25, "velocity": "low"},
    "SKU-FAB-006": {"name": "Cotton Silk Blend Roll 25m", "quantity": 0, "min_threshold": 30, "velocity": "high"},
    "SKU-FAB-007": {"name": "Jute Fabric Roll 20m", "quantity": 40, "min_threshold": 20, "velocity": "low"},
    "SKU-FAB-008": {"name": "Chiffon Fabric Roll 15m", "quantity": 0, "min_threshold": 25, "velocity": "medium"},
}

CUSTOMERS = {
    "CUST001": {"name": "Acme Corp", "email": "orders@acme.com", "phone": "+1-555-0100", "industry": "electronics", "tier": "gold"},
    "CUST002": {"name": "GlobalTech Inc", "email": "logistics@globaltech.com", "phone": "+1-555-0200", "industry": "electronics", "tier": "silver"},
    "CUST003": {"name": "FabIndia Textiles", "email": "purchase@fabindia.com", "phone": "+1-555-0300", "industry": "textile", "tier": "platinum"},
    "CUST004": {"name": "Heritage Fabrics", "email": "orders@heritagefabrics.com", "phone": "+1-555-0400", "industry": "textile", "tier": "gold"},
    "CUST005": {"name": "Bombay Dyeing", "email": "procurement@bombaydyeing.com", "phone": "+1-555-0500", "industry": "textile", "tier": "silver"},
    "CUST006": {"name": "Reliance Textiles", "email": "supply@reliancetextiles.com", "phone": "+1-555-0600", "industry": "textile", "tier": "platinum"},
    "CUST007": {"name": "TechHub Solutions", "email": "orders@techhub.com", "phone": "+1-555-0700", "industry": "electronics", "tier": "bronze"},
    "CUST008": {"name": "GreenPack Logistics", "email": "warehouse@greenpack.com", "phone": "+1-555-0800", "industry": "packaging", "tier": "silver"},
    "CUST009": {"name": "SafeWear Industries", "email": "inventory@safewear.com", "phone": "+1-555-0900", "industry": "safety", "tier": "gold"},
    "CUST010": {"name": "Lotus Silks", "email": "buy@lotussilks.com", "phone": "+1-555-1000", "industry": "textile", "tier": "gold"},
    "CUST011": {"name": "Arrow Electronics", "email": "parts@arrowelec.com", "phone": "+1-555-1100", "industry": "electronics", "tier": "silver"},
    "CUST012": {"name": "Pinnacle Garments", "email": "orders@pinnaclegarments.com", "phone": "+1-555-1200", "industry": "textile", "tier": "bronze"},
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
    {"order_id": "ORD-3001", "customer": "CUST004", "items": [{"sku": "SKU-FAB-001", "qty": 30}, {"sku": "SKU-FAB-007", "qty": 20}], "status": "shipped", "tracking_number": "TRK30001", "date": "2026-06-20"},
    {"order_id": "ORD-3002", "customer": "CUST005", "items": [{"sku": "SKU-FAB-003", "qty": 50}], "status": "delivered", "tracking_number": "TRK30002", "date": "2026-06-15"},
    {"order_id": "ORD-3003", "customer": "CUST006", "items": [{"sku": "SKU-FAB-001", "qty": 200}, {"sku": "SKU-FAB-005", "qty": 100}], "status": "shipped", "tracking_number": "TRK20001", "date": "2026-06-22"},
    {"order_id": "ORD-3004", "customer": "CUST007", "items": [{"sku": "SKU-ELEC-004", "qty": 150}, {"sku": "SKU-ELEC-005", "qty": 80}], "status": "processing", "tracking_number": "TRK30003", "date": "2026-06-29"},
    {"order_id": "ORD-3005", "customer": "CUST008", "items": [{"sku": "SKU-PACK-002", "qty": 500}, {"sku": "SKU-PACK-003", "qty": 300}], "status": "shipped", "tracking_number": "TRK30004", "date": "2026-06-26"},
    {"order_id": "ORD-3006", "customer": "CUST009", "items": [{"sku": "SKU-WEAR-002", "qty": 200}, {"sku": "SKU-WEAR-003", "qty": 150}], "status": "pending", "tracking_number": None, "date": "2026-06-30"},
    {"order_id": "ORD-3007", "customer": "CUST010", "items": [{"sku": "SKU-FAB-002", "qty": 60}, {"sku": "SKU-FAB-008", "qty": 40}], "status": "delayed", "tracking_number": "TRK20004", "date": "2026-06-24"},
    {"order_id": "ORD-3008", "customer": "CUST011", "items": [{"sku": "SKU-ELEC-002", "qty": 200}, {"sku": "SKU-ELEC-005", "qty": 100}], "status": "shipped", "tracking_number": "TRK10001", "date": "2026-06-21"},
    {"order_id": "ORD-3009", "customer": "CUST012", "items": [{"sku": "SKU-FAB-006", "qty": 25}, {"sku": "SKU-FAB-001", "qty": 15}], "status": "processing", "tracking_number": "TRK30003", "date": "2026-06-28"},
    {"order_id": "ORD-3010", "customer": "CUST010", "items": [{"sku": "SKU-FAB-002", "qty": 90}], "status": "shipped", "tracking_number": "TRK30001", "date": "2026-05-25"},
    {"order_id": "ORD-3011", "customer": "CUST004", "items": [{"sku": "SKU-FAB-007", "qty": 50}], "status": "delivered", "tracking_number": "TRK30002", "date": "2026-05-20"},
    {"order_id": "ORD-3012", "customer": "CUST003", "items": [{"sku": "SKU-FAB-005", "qty": 60}, {"sku": "SKU-FAB-003", "qty": 30}], "status": "shipped", "tracking_number": "TRK20002", "date": "2026-05-15"},
    {"order_id": "ORD-3013", "customer": "CUST006", "items": [{"sku": "SKU-FAB-001", "qty": 150}], "status": "shipped", "tracking_number": "TRK20001", "date": "2026-05-10"},
    {"order_id": "ORD-3014", "customer": "CUST001", "items": [{"sku": "SKU-ELEC-004", "qty": 60}], "status": "delivered", "tracking_number": "TRK10003", "date": "2026-04-28"},
    {"order_id": "ORD-3015", "customer": "CUST002", "items": [{"sku": "SKU-ELEC-003", "qty": 40}], "status": "delivered", "tracking_number": "TRK10003", "date": "2026-04-15"},
    {"order_id": "ORD-3016", "customer": "CUST003", "items": [{"sku": "SKU-FAB-001", "qty": 80}, {"sku": "SKU-FAB-002", "qty": 40}], "status": "shipped", "tracking_number": "TRK20001", "date": "2026-04-10"},
    {"order_id": "ORD-3017", "customer": "CUST007", "items": [{"sku": "SKU-ELEC-001", "qty": 120}], "status": "delivered", "tracking_number": "TRK10003", "date": "2026-03-25"},
    {"order_id": "ORD-3018", "customer": "CUST011", "items": [{"sku": "SKU-ELEC-002", "qty": 80}, {"sku": "SKU-ELEC-005", "qty": 50}], "status": "shipped", "tracking_number": "TRK10001", "date": "2026-03-20"},
    {"order_id": "ORD-3019", "customer": "CUST009", "items": [{"sku": "SKU-WEAR-001", "qty": 300}], "status": "shipped", "tracking_number": "TRK10004", "date": "2026-03-15"},
    {"order_id": "ORD-3020", "customer": "CUST003", "items": [{"sku": "SKU-FAB-008", "qty": 60}], "status": "shipped", "tracking_number": "TRK20001", "date": "2026-03-10"},
]

SUPPLIERS = {
    "SUP-001": {"name": "Fabric Mills India", "lead_time_days": 14, "min_order_qty": 50, "categories": ["FAB"], "rating": 4.5, "price_rating": "competitive"},
    "SUP-002": {"name": "Tech Components Ltd", "lead_time_days": 7, "min_order_qty": 20, "categories": ["ELEC"], "rating": 4.2, "price_rating": "premium"},
    "SUP-003": {"name": "PackWell Supplies", "lead_time_days": 5, "min_order_qty": 100, "categories": ["PACK"], "rating": 4.8, "price_rating": "budget"},
    "SUP-004": {"name": "SafeGear Manufacturing", "lead_time_days": 10, "min_order_qty": 50, "categories": ["WEAR"], "rating": 4.0, "price_rating": "competitive"},
    "SUP-005": {"name": "Luxury Fabrics Co", "lead_time_days": 21, "min_order_qty": 10, "categories": ["FAB"], "rating": 4.9, "price_rating": "premium"},
    "SUP-006": {"name": "SilkRoute Exports", "lead_time_days": 18, "min_order_qty": 25, "categories": ["FAB"], "rating": 4.3, "price_rating": "competitive"},
    "SUP-007": {"name": "ElectroWorld Distributors", "lead_time_days": 10, "min_order_qty": 30, "categories": ["ELEC"], "rating": 3.8, "price_rating": "budget"},
    "SUP-008": {"name": "EcoPack Solutions", "lead_time_days": 7, "min_order_qty": 50, "categories": ["PACK"], "rating": 4.6, "price_rating": "competitive"},
}

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
    lines = ["Orders:"]
    for o in orders:
        cname = CUSTOMERS.get(o["customer"], {}).get("name", o["customer"])
        items_str = ", ".join(f"{_item_name(i['sku'])} x{i['qty']}" for i in o["items"])
        tracking = f" (Track: {o['tracking_number']})" if o["tracking_number"] else ""
        lines.append(f"  * {o['order_id']} - {cname} - {o['status'].upper()}{tracking}")
        lines.append(f"    Items: {items_str}")
    return "\n".join(lines)


CUSTOMER_NAME_TO_ID = {v["name"].lower(): k for k, v in CUSTOMERS.items()}


def _find_or_create_customer(name: str) -> str:
    lower = name.strip().lower()
    if lower in CUSTOMER_NAME_TO_ID:
        return CUSTOMER_NAME_TO_ID[lower]
    existing_ids = sorted(CUSTOMERS.keys())
    new_id = f"CUST{int(existing_ids[-1].replace('CUST', '')) + 1:03d}"
    CUSTOMERS[new_id] = {"name": name.strip(), "email": f"orders@{name.strip().replace(' ', '').lower()}.com", "phone": "", "industry": "unknown", "tier": "bronze"}
    CUSTOMER_NAME_TO_ID[name.strip().lower()] = new_id
    return new_id


def _ensure_product(name: str) -> str | None:
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
    items_detail = "\n".join(f"  * {_item_name(i['sku'])} x{i['qty']}" for i in items)
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
    items_str = "\n".join(f"  * {_item_name(i['sku'])} x{i['qty']}" for i in order["items"])
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
    delay = f" - Reason: {s.get('delay_reason', 'N/A')}" if s.get("status") == "delayed" else ""
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
    """Check current inventory quantity and status for a given SKU."""
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
    "elec": "ELEC", "electronic": "ELEC", "keyboard": "ELEC", "usb": "ELEC", "monitor": "ELEC", "speaker": "ELEC", "charger": "ELEC", "laptop": "ELEC",
    "wear": "WEAR", "glove": "WEAR", "safety": "WEAR", "goggle": "WEAR", "apron": "WEAR",
    "pack": "PACK", "box": "PACK", "corrugated": "PACK", "tape": "PACK", "bubble": "PACK", "wrap": "PACK",
    "fab": "FAB", "fabric": "FAB", "cotton": "FAB", "silk": "FAB", "linen": "FAB", "polyester": "FAB", "denim": "FAB", "jute": "FAB", "chiffon": "FAB",
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
        flag = " LOW" if item["quantity"] < item["min_threshold"] else ""
        lines.append(f"  {sku} - {item['name']} - qty: {item['quantity']}{flag}")
    return "\n".join(lines)


def restock_product(name_or_sku: str, quantity: int) -> str:
    """Add stock to an existing product. Provide the product name or SKU and the quantity to add."""
    sku = _find_sku(name_or_sku)
    if not sku:
        available = "\n".join(f"  {s} - {i['name']}" for s, i in sorted(INVENTORY.items()))
        return f"Product '{name_or_sku}' not found. Available products:\n{available}"
    item = INVENTORY[sku]
    old_qty = item["quantity"]
    item["quantity"] = old_qty + quantity
    return f"Restocked {item['name']} ({sku}): {old_qty} -> {item['quantity']} (+{quantity})"


def add_product(name: str, quantity: int, min_threshold: int = 50, velocity: str = "medium") -> str:
    """Add a new product to inventory. SKU is auto-generated. Velocity: high/medium/low."""
    for sku, item in INVENTORY.items():
        if item["name"].lower() == name.lower():
            return f"Product '{name}' already exists as {sku}. Use restock_product to add stock."
    category = _detect_category(name)
    sku = _next_sku(category)
    INVENTORY[sku] = {"name": name, "quantity": quantity, "min_threshold": min_threshold, "velocity": velocity}
    return f"Added new product: {sku} - {name} (qty: {quantity}, min: {min_threshold}, velocity: {velocity})"


# ============================================================
# INVENTORY INTELLIGENCE ENGINE
# ============================================================

ORDER_HISTORY = []
for o in ORDERS:
    for item in o["items"]:
        ORDER_HISTORY.append({"sku": item["sku"], "qty": item["qty"], "date": o["date"], "customer": o["customer"]})

PENDING_REPLENISHMENTS: dict[str, dict] = {}

from .forecasting import calculate_reorder_qty, forecast_daily_demand


def forecast_demand(sku: str, days: int = 30) -> str:
    """Forecast demand for a product SKU based on historical order data, seasonal trends, and customer buying patterns.
    Returns projected daily demand, safety stock, and reorder point."""
    item = INVENTORY.get(sku)
    if not item:
        return f"Product '{sku}' not found in inventory."
    result = calculate_reorder_qty(sku, item["quantity"], ORDER_HISTORY)
    lines = [
        f"Demand Forecast for {item['name']} ({sku}):",
        f"  Current Stock: {item['quantity']} units",
        f"  Forecasted Daily Demand: {result['daily_demand']} units/day",
        f"  Safety Stock: {result['safety_stock']} units (service level: 95%)",
        f"  Reorder Point: {result['reorder_point']} units",
        f"  Reorder Needed: {'YES' if result['needs_reorder'] else 'No'}",
    ]
    if result['needs_reorder']:
        lines.append(f"  Suggested Reorder Qty: {result['reorder_qty']} units")
        lines.append(f"  Reason: {result['reason']}")
    lines.append(f"  ({days}-day projected consumption: {round(result['daily_demand'] * days, 1)} units)")
    return "\n".join(lines)


def analyze_customer_demand(customer_id: str = "") -> str:
    """Analyze buying patterns for a customer or all customers. Shows order frequency, preferred product categories, growth trends, and partnership potential."""
    customers_to_analyze = [customer_id] if customer_id else list(CUSTOMERS.keys())
    results = []
    for cid in customers_to_analyze:
        if cid not in CUSTOMERS:
            continue
        c = CUSTOMERS[cid]
        customer_orders = [o for o in ORDERS if o["customer"] == cid]
        total_orders = len(customer_orders)
        if total_orders == 0:
            results.append(f"{c['name']} ({cid}): No order history.")
            continue
        total_qty = sum(item["qty"] for o in customer_orders for item in o["items"])
        categories = {}
        for o in customer_orders:
            for item in o["items"]:
                inv = INVENTORY.get(item["sku"], {})
                cat = item["sku"].split("-")[1] if "-" in item["sku"] else "GEN"
                categories[cat] = categories.get(cat, 0) + item["qty"]
        cat_str = ", ".join(f"{cat}: {qty}" for cat, qty in sorted(categories.items(), key=lambda x: -x[1]))
        recent = [o for o in customer_orders if o["date"] >= "2026-05-01"]
        recent3 = [o for o in customer_orders if "2026-03-01" <= o["date"] < "2026-05-01"]
        growth = "growing" if len(recent) > len(recent3) else ("stable" if len(recent) == len(recent3) else "declining")
        results.append(
            f"  {c['name']} ({cid}) - Tier: {c.get('tier', 'bronze')} | Industry: {c.get('industry', 'unknown')}\n"
            f"    Orders: {total_orders} | Total Units: {total_qty}\n"
            f"    Categories: {cat_str}\n"
            f"    Trend: {growth} (Recent: {len(recent)} vs Prior: {len(recent3)} orders)\n"
            f"    Partnership Potential: {'HIGH' if growth == 'growing' and total_orders >= 3 else 'MEDIUM' if total_orders >= 2 else 'LOW'}"
        )
    header = f"Customer Demand Analysis{' for ' + CUSTOMERS.get(customer_id, {}).get('name', '') if customer_id else ' (All)'}:"
    return header + "\n" + "\n\n".join(results)


def get_reorder_recommendations() -> str:
    """Scan all products and recommend which ones need reordering based on forecast, stock levels, velocity, and seasonality."""
    lines = ["Reorder Recommendations (auto-calculated):"]
    needs_reorder = False
    for sku in sorted(INVENTORY):
        item = INVENTORY[sku]
        result = calculate_reorder_qty(sku, item["quantity"], ORDER_HISTORY)
        if result["needs_reorder"]:
            needs_reorder = True
            lines.append(
                f"  {item['name']} ({sku}):"
                f"\n    Current: {item['quantity']} | Forecast: {result['daily_demand']}/day"
                f"\n    Safety: {result['safety_stock']} | Reorder Point: {result['reorder_point']}"
                f"\n    Suggested Order: {result['reorder_qty']} units"
                f"\n    Reason: {result['reason']}"
            )
    if not needs_reorder:
        lines.append("  All products have sufficient stock.")
    return "\n".join(lines)


def auto_replenish(sku: str, auto_approve: bool = False) -> str:
    """Calculate and prepare a replenishment order for a specific SKU.
    This requires human approval before execution. Returns the replenishment proposal.
    Use confirm_replenish() after approval to execute."""
    item = INVENTORY.get(sku)
    if not item:
        return f"Product '{sku}' not found in inventory."
    result = calculate_reorder_qty(sku, item["quantity"], ORDER_HISTORY)
    if not result["needs_reorder"]:
        return f"{item['name']} ({sku}): No replenishment needed. Stock: {item['quantity']}, Reorder Point: {result['reorder_point']}."
    PENDING_REPLENISHMENTS[sku] = {
        "name": item["name"],
        "current_qty": item["quantity"],
        "reorder_qty": result["reorder_qty"],
        "forecast_qty": result["daily_demand"],
        "safety_stock": result["safety_stock"],
        "reorder_point": result["reorder_point"],
        "reason": result["reason"],
        "status": "pending_approval",
        "timestamp": datetime.now().isoformat(),
    }
    return (
        f"[REPLENISHMENT_PROPOSAL] {item['name']} ({sku})\n"
        f"  Current Stock: {item['quantity']} units\n"
        f"  Suggested Reorder: {result['reorder_qty']} units\n"
        f"  Forecasted Demand: {result['daily_demand']} units/day\n"
        f"  Safety Stock: {result['safety_stock']} units\n"
        f"  Reason: {result['reason']}\n"
        f"  Est. Monthly Consumption: {round(result['daily_demand'] * 30, 1)} units\n"
        f"Status: PENDING HUMAN APPROVAL\n"
        f"Please type 'approve' or 'yes' to proceed with this replenishment."
    )


def confirm_replenish(sku: str) -> str:
    """Execute a previously proposed replenishment after human approval. If no pending replenishment exists, proposes one."""
    pending = PENDING_REPLENISHMENTS.get(sku)
    if not pending or pending.get("status") != "pending_approval":
        result = calculate_reorder_qty(sku, INVENTORY.get(sku, {}).get("quantity", 0), ORDER_HISTORY)
        if not result["needs_reorder"]:
            return "No replenishment pending and no reorder needed."
        return auto_replenish(sku)
    qty = pending["reorder_qty"]
    msg = restock_product(sku, qty)
    PENDING_REPLENISHMENTS[sku]["status"] = "approved"
    return f"[APPROVED] {msg}\nSupplier notified. Estimated delivery in 14 days."


def reject_replenish(sku: str, reason: str = "") -> str:
    """Reject a pending replenishment proposal without executing it."""
    pending = PENDING_REPLENISHMENTS.get(sku)
    if not pending or pending.get("status") != "pending_approval":
        return "No pending replenishment found for this product."
    PENDING_REPLENISHMENTS[sku]["status"] = "rejected"
    PENDING_REPLENISHMENTS[sku]["rejection_reason"] = reason
    PENDING_REPLENISHMENTS[sku]["rejected_at"] = datetime.now().isoformat()
    return f"[REJECTED] Replenishment for {pending['name']} ({sku}) has been cancelled. Reason: {reason or 'No reason provided'}."


def suggest_partnerships() -> str:
    """Analyze customer order data and suggest which companies have strong partnership potential based on growth, order frequency, and category diversity."""
    scores = []
    for cid, c in CUSTOMERS.items():
        customer_orders = [o for o in ORDERS if o["customer"] == cid]
        if len(customer_orders) < 2:
            continue
        recent = [o for o in customer_orders if o["date"] >= "2026-05-01"]
        prior = [o for o in customer_orders if "2026-03-01" <= o["date"] < "2026-05-01"]
        growth_rate = (len(recent) - len(prior)) / max(len(prior), 1)
        frequency = len(customer_orders) / 4.0
        cats = set()
        for o in customer_orders:
            for item in o["items"]:
                cat = item["sku"].split("-")[1] if "-" in item["sku"] else "GEN"
                cats.add(cat)
        diversity = len(cats) / 5.0
        score = 0.4 * min(growth_rate + 1, 2) + 0.3 * min(frequency / 3, 1) + 0.2 * min(diversity, 1) + 0.1 * min(1, 1 - len(recent) / max(len(customer_orders), 1))
        scores.append({
            "cid": cid, "name": c["name"], "industry": c.get("industry", "unknown"), "tier": c.get("tier", "bronze"),
            "score": round(score * 100), "growth": "high" if growth_rate > 0.3 else ("medium" if growth_rate > 0 else "stable"),
            "orders": len(customer_orders), "categories": ", ".join(sorted(cats)),
            "total_units": sum(item["qty"] for o in customer_orders for item in o["items"]),
        })
    scores.sort(key=lambda x: -x["score"])
    lines = [
        "Partnership Recommendations (ranked by growth-weighted score):",
        "  Algorithm: Growth(40%) + Frequency(30%) + Diversity(20%) + Recency(10%)",
    ]
    for i, s in enumerate(scores, 1):
        badge = "[RECOMMENDED]" if s["score"] >= 60 else "[POTENTIAL]" if s["score"] >= 35 else "[EMERGING]"
        lines.append(
            f"\n  #{i} {badge} {s['name']} ({s['score']}/100)"
            f"\n     Industry: {s['industry']} | Tier: {s['tier']}"
            f"\n     Orders: {s['orders']} | Units: {s['total_units']}"
            f"\n     Growth: {s['growth']} | Categories: {s['categories']}"
        )
    strategic = [s for s in scores if s["score"] >= 60]
    if strategic:
        lines.append(f"\nStrategic Partners (Score >= 60): {', '.join(s['name'] for s in strategic)}")
    return "\n".join(lines)


def search_company_trends(query: str = "") -> str:
    """Search for company trends and market insights across our customer database.
    Returns growth patterns, industry health, and partnership readiness for companies matching the query."""
    results = []
    query_lower = query.lower().strip() if query else ""
    for cid, c in CUSTOMERS.items():
        if query_lower and query_lower not in c["name"].lower() and query_lower not in c.get("industry", "").lower():
            continue
        customer_orders = [o for o in ORDERS if o["customer"] == cid]
        if not customer_orders:
            continue
        total_units = sum(item["qty"] for o in customer_orders for item in o["items"])
        recent_orders = [o for o in customer_orders if o["date"] >= "2026-06-01"]
        trending = len(recent_orders) >= 2
        industry_trends = {
            "textile": "High demand expected Q4 2026 (festival season). Wedding season driving silk/cotton up.",
            "electronics": "Back-to-school and holiday season demand rising. Component shortages easing.",
            "packaging": "Steady growth driven by e-commerce boom. Corrugated demand up 15% YoY.",
            "safety": "Regulatory compliance driving consistent demand. Industrial safety market growing 8% annually.",
        }
        trend = industry_trends.get(c.get("industry", ""), "Stable market conditions.")
        results.append(
            f"  {c['name']} ({cid})\n"
            f"    Industry: {c.get('industry', 'N/A')} | Tier: {c.get('tier', 'bronze')}\n"
            f"    Total Orders: {len(customer_orders)} | Total Units: {total_units}\n"
            f"    Recent Activity (June): {len(recent_orders)} orders {'[TRENDING UP]' if trending else ''}\n"
            f"    Market Insight: {trend}"
        )
    if not results:
        return f"No companies found matching '{query}'. Try searching by name or industry."
    header = f"Company Trends & Market Insights{' for: ' + query if query else ' (All Customers)'}:"
    return header + "\n\n" + "\n\n".join(results)


# ============================================================
# ORDER PRIORITIZATION & URGENCY ENGINE
# ============================================================

PRODUCT_COSTS = {
    "SKU-ELEC-001": {"cost": 12.00, "sell": 29.99, "weight_kg": 0.5},
    "SKU-ELEC-002": {"cost": 5.50, "sell": 18.99, "weight_kg": 0.2},
    "SKU-ELEC-003": {"cost": 18.00, "sell": 45.00, "weight_kg": 1.2},
    "SKU-ELEC-004": {"cost": 8.00, "sell": 24.99, "weight_kg": 0.4},
    "SKU-ELEC-005": {"cost": 9.50, "sell": 22.99, "weight_kg": 0.3},
    "SKU-WEAR-001": {"cost": 3.00, "sell": 8.99, "weight_kg": 0.1},
    "SKU-WEAR-002": {"cost": 4.50, "sell": 12.99, "weight_kg": 0.15},
    "SKU-WEAR-003": {"cost": 7.00, "sell": 18.50, "weight_kg": 0.4},
    "SKU-PACK-001": {"cost": 0.75, "sell": 2.50, "weight_kg": 0.3},
    "SKU-PACK-002": {"cost": 1.20, "sell": 3.99, "weight_kg": 0.1},
    "SKU-PACK-003": {"cost": 2.00, "sell": 5.99, "weight_kg": 0.2},
    "SKU-FAB-001": {"cost": 25.00, "sell": 55.00, "weight_kg": 5.0},
    "SKU-FAB-002": {"cost": 40.00, "sell": 89.00, "weight_kg": 3.0},
    "SKU-FAB-003": {"cost": 30.00, "sell": 65.00, "weight_kg": 4.0},
    "SKU-FAB-004": {"cost": 18.00, "sell": 42.00, "weight_kg": 4.5},
    "SKU-FAB-005": {"cost": 22.00, "sell": 48.00, "weight_kg": 3.5},
    "SKU-FAB-006": {"cost": 35.00, "sell": 75.00, "weight_kg": 2.5},
    "SKU-FAB-007": {"cost": 15.00, "sell": 38.00, "weight_kg": 3.0},
    "SKU-FAB-008": {"cost": 28.00, "sell": 62.00, "weight_kg": 2.0},
}

SHIPPING_RATES = {
    "FedEx": {"base": 5.99, "per_kg": 2.50},
    "UPS": {"base": 4.99, "per_kg": 3.00},
    "DHL": {"base": 6.99, "per_kg": 2.00},
    "Maersk": {"base": 15.00, "per_kg": 1.00},
    "BlueDart": {"base": 3.99, "per_kg": 2.00},
    "Delhivery": {"base": 2.99, "per_kg": 1.50},
    "EcomExpress": {"base": 3.50, "per_kg": 1.80},
}

HANDLING_COST = 2.50
STORAGE_COST_PER_UNIT = 0.05

URGENCY_TRIGGER_WORDS = ["rush", "urgent", "asap", "priority", "critical", "emergency", "expedite", "fast", "immediate", "quick"]

DEFAULT_ORDER_NOTES = {
    "ORD-1004": "Customer requested expedited shipping - URGENT delivery needed",
    "ORD-2004": "Client flagged as critical - delay causing production halt at factory",
    "ORD-3004": "RUSH order - new product launch dependent on this delivery",
    "ORD-3006": "Safety equipment needed urgently - regulatory deadline approaching",
    "ORD-3009": "Seasonal collection launch - PRIORITY handling requested",
    "ORD-1002": "Customer complaint about previous delay - needs priority resolution",
    "ORD-1005": "Normal processing",
}


def _tier_weight(tier: str) -> int:
    return {"platinum": 5, "gold": 4, "silver": 3, "bronze": 2}.get(tier, 1)


def _priority_score(order: dict) -> dict:
    cid = order["customer"]
    c = CUSTOMERS.get(cid, {})
    tier_w = _tier_weight(c.get("tier", "bronze")) / 5.0
    notes = DEFAULT_ORDER_NOTES.get(order["order_id"], "").lower()
    urgency = sum(1 for w in URGENCY_TRIGGER_WORDS if w in notes) / len(URGENCY_TRIGGER_WORDS)
    delay_risk = {"delayed": 1.0, "pending": 0.7, "processing": 0.4, "shipped": 0.0, "delivered": 0.0}.get(order["status"], 0.3)
    total_value = sum(
        PRODUCT_COSTS.get(item["sku"], {}).get("sell", 10) * item["qty"]
        for item in order["items"]
    )
    all_values = [
        sum(PRODUCT_COSTS.get(item["sku"], {}).get("sell", 10) * item["qty"] for item in o["items"])
        for o in ORDERS
    ]
    value_score = min(total_value / (max(all_values) if all_values else 1000), 1.0)
    score = 0.35 * tier_w + 0.25 * urgency + 0.20 * delay_risk + 0.10 * value_score + 0.10 * (1 - delay_risk)
    if score >= 0.55:
        label = "CRITICAL"
    elif score >= 0.45:
        label = "URGENT"
    elif score >= 0.30:
        label = "PRIORITY"
    else:
        label = "STANDARD"
    return {"score": round(score, 2), "label": label, "urgency_detected": urgency > 0, "delay_risk": delay_risk, "value_score": round(value_score, 2)}


def prioritize_orders(status_filter: str = "") -> str:
    """Analyze all orders and rank them by priority score using tier weight, urgency, delay risk, and order value.
    Returns a ranked list with CRITICAL/URGENT/PRIORITY/STANDARD labels."""
    result = []
    for o in ORDERS:
        if status_filter and o["status"] != status_filter:
            continue
        ps = _priority_score(o)
        cname = CUSTOMERS.get(o["customer"], {}).get("name", o["customer"])
        note = DEFAULT_ORDER_NOTES.get(o["order_id"], "")
        note_flag = f" [NOTE: {note}]" if note else ""
        result.append({
            "order_id": o["order_id"],
            "customer": cname,
            "status": o["status"],
            "label": ps["label"],
            "score": ps["score"],
            "urgent": ps["urgency_detected"],
            "note": note,
        })
    result.sort(key=lambda x: (-x["score"], x["order_id"]))
    lines = ["Order Priority Queue (ranked by urgency):"]
    lines.append("  Algorithm: Tier(35%) + Urgency(25%) + DelayRisk(20%) + Value(10%) + Recency(10%)")
    lines.append(f"  Thresholds: CRITICAL >= 0.55 | URGENT >= 0.45 | PRIORITY >= 0.30 | STANDARD < 0.30")
    lines.append("")
    for r in result:
        badge = "[CRITICAL]" if r["label"] == "CRITICAL" else "[URGENT]" if r["label"] == "URGENT" else "[PRIORITY]" if r["label"] == "PRIORITY" else ""
        lines.append(f"  {badge} {r['order_id']} - {r['customer']} ({r['status']})")
        lines.append(f"     Priority Score: {r['score']}")
        if r["note"]:
            lines.append(f"     Note: {r['note']}")
    return "\n".join(lines)


def push_urgent_orders() -> str:
    """Identify and push CRITICAL and URGENT orders to the front of the queue.
    Returns a prioritized action plan with recommended SLA-based handling."""
    urgent = []
    for o in ORDERS:
        if o["status"] in ("delivered", "shipped"):
            continue
        ps = _priority_score(o)
        if ps["label"] in ("CRITICAL", "URGENT"):
            cname = CUSTOMERS.get(o["customer"], {}).get("name", o["customer"])
            note = DEFAULT_ORDER_NOTES.get(o["order_id"], "")
            urgent.append({
                "order_id": o["order_id"], "customer": cname, "status": o["status"],
                "label": ps["label"], "score": ps["score"], "note": note,
                "items": o["items"],
            })
    urgent.sort(key=lambda x: -x["score"])
    if not urgent:
        return "No urgent orders currently require priority pushing."
    tier_map = {"CRITICAL": "SLA: Within 24 hours", "URGENT": "SLA: Within 48 hours"}
    lines = ["[ALERT] URGENT ORDER PUSH - Action Required:"]
    lines.append(f"  {len(urgent)} orders flagged for immediate priority handling\n")
    for u in urgent:
        sla = tier_map.get(u["label"], "SLA: Standard")
        items_detail = ", ".join(f"{INVENTORY.get(i['sku'], {}).get('name', i['sku'])} x{i['qty']}" for i in u["items"])
        lines.append(f"  [{u['label']}] {u['order_id']} - {u['customer']}")
        lines.append(f"     Status: {u['status']} | Score: {u['score']}")
        lines.append(f"     {sla}")
        lines.append(f"     Items: {items_detail}")
        if u["note"]:
            lines.append(f"     Reason: {u['note']}")
        lines.append("")
    lines.append("Recommended Actions:")
    lines.append("  1. Assign dedicated handler for CRITICAL orders")
    lines.append("  2. Notify warehouse team for immediate pick-pack")
    lines.append("  3. Choose fastest carrier (check carrier_optimize)")
    lines.append("  4. Send proactive customer notification")
    return "\n".join(lines)


def customer_360(customer_id: str) -> str:
    """Get a unified 360-degree view of a customer including profile, order history, profitability, buying patterns, partnership score, and predictions."""
    c = CUSTOMERS.get(customer_id)
    if not c:
        return f"Customer '{customer_id}' not found."
    customer_orders = [o for o in ORDERS if o["customer"] == customer_id]
    total_orders = len(customer_orders)
    total_units = sum(item["qty"] for o in customer_orders for item in o["items"])
    status_counts = {}
    for o in customer_orders:
        status_counts[o["status"]] = status_counts.get(o["status"], 0) + 1
    cat_totals = {}
    for o in customer_orders:
        for item in o["items"]:
            cat = item["sku"].split("-")[1] if "-" in item["sku"] else "GEN"
            cat_totals[cat] = cat_totals.get(cat, 0) + item["qty"]
    top_cat = max(cat_totals, key=cat_totals.get) if cat_totals else "N/A"
    recent = [o for o in customer_orders if o["date"] >= "2026-05-01"]
    prior = [o for o in customer_orders if "2026-03-01" <= o["date"] < "2026-05-01"]
    growth = "growing" if len(recent) > len(prior) else ("stable" if len(recent) == len(prior) else "declining")
    revenue = 0
    cogs_total = 0
    shipping_total = 0
    for o in customer_orders:
        for item in o["items"]:
            costs = PRODUCT_COSTS.get(item["sku"], {"cost": 0, "sell": 0})
            revenue += costs["sell"] * item["qty"]
            cogs_total += costs["cost"] * item["qty"]
        s = SHIPMENTS.get(o.get("tracking_number", ""), {})
        carrier = s.get("carrier", "FedEx")
        rate = SHIPPING_RATES.get(carrier, SHIPPING_RATES["FedEx"])
        total_kg = sum(PRODUCT_COSTS.get(i["sku"], {}).get("weight_kg", 0.5) * i["qty"] for i in o["items"])
        shipping_total += rate["base"] + rate["per_kg"] * total_kg
    handling_total = total_orders * HANDLING_COST
    storage_total = total_units * STORAGE_COST_PER_UNIT * 30
    total_cost = cogs_total + shipping_total + handling_total + storage_total
    profit = revenue - total_cost
    margin = (profit / revenue * 100) if revenue > 0 else 0
    overdue = [o for o in customer_orders if o["status"] == "delayed"]
    lines = [
        "[SEARCH] CUSTOMER 360 VIEW",
        "=" * 50,
        f"  {c['name']} ({customer_id})",
        f"  Industry: {c.get('industry', 'N/A')} | Tier: {c.get('tier', 'bronze')}",
        f"  Contact: {c.get('email', 'N/A')} | Phone: {c.get('phone', 'N/A')}",
        "",
        "  [ORDER PROFILE]",
        f"    Total Orders: {total_orders} | Total Units: {total_units}",
        f"    Status Breakdown: {', '.join(f'{k}: {v}' for k, v in sorted(status_counts.items()))}",
        f"    Top Category: {top_cat} ({cat_totals.get(top_cat, 0)} units)",
        f"    Growth Trend: {growth.upper()} (Recent: {len(recent)} vs Prior: {len(prior)} orders)",
        f"    Overdue Orders: {len(overdue)}",
        "",
        "  [FINANCIAL SUMMARY]",
        f"    Revenue: ${revenue:,.2f}",
        f"    COGS: ${cogs_total:,.2f}",
        f"    Shipping: ${shipping_total:,.2f}",
        f"    Handling: ${handling_total:,.2f}",
        f"    Storage: ${storage_total:,.2f}",
        f"    Total Cost: ${total_cost:,.2f}",
        f"    Net Profit: ${profit:,.2f}",
        f"    Profit Margin: {margin:.1f}%",
        f"    {'[OK] PROFITABLE' if profit > 0 else '[ALERT] AT RISK'}",
        "",
        "  [RECENT ORDERS]",
    ]
    for o in sorted(customer_orders, key=lambda x: x["date"], reverse=True)[:5]:
        items_short = ", ".join(f"{INVENTORY.get(i['sku'], {}).get('name', i['sku'])[:20]} x{i['qty']}" for i in o["items"])
        lines.append(f"    {o['order_id']} ({o['date']}) - {o['status'].upper()} - {items_short}")
    lines.append("")
    lines.append("  [PARTNERSHIP SCORE]")
    partner_score = min(total_orders * 15 + (growth == "growing") * 20 + _tier_weight(c.get("tier", "bronze")) * 10, 100)
    lines.append(f"    Score: {partner_score}/100 ({'HIGH' if partner_score >= 60 else 'MEDIUM' if partner_score >= 35 else 'LOW'})")
    if profit < 0:
        lines.append(f"    [ALERT] Note: Account showing loss. Review minimize_losses() for recovery options.")
    else:
        lines.append(f"    [OK] Note: Profitable customer. Consider loyalty program upgrade.")
    lines.append("")
    lines.append("  [PREDICTED NEXT ORDER]")
    avg_interval = max(1, len(customer_orders) // max(1, (max(1, len(customer_orders)) - 1)))
    predicted_product = next((INVENTORY.get(i["sku"], {}).get("name") for o in customer_orders for i in o["items"] if i["sku"] in [x["sku"] for x in customer_orders[-1]["items"]]), "N/A")
    lines.append(f"    Estimated: ~{avg_interval} orders/month")
    lines.append(f"    Likely Product: {top_cat.replace('ELEC', 'Electronics').replace('FAB', 'Fabric').replace('PACK', 'Packaging').replace('WEAR', 'Safety Wear')}")
    lines.append(f"    Est. Value: ${cat_totals.get(top_cat, 0) * 20 / max(1, total_orders):,.0f}")
    return "\n".join(lines)


def calculate_order_margins(order_id: str) -> str:
    """Calculate detailed profit margin breakdown for a specific order including revenue, COGS, shipping, handling, storage costs, and net profit."""
    order = next((o for o in ORDERS if o["order_id"] == order_id), None)
    if not order:
        return f"Order '{order_id}' not found."
    cname = CUSTOMERS.get(order["customer"], {}).get("name", order["customer"])
    revenue = 0
    cogs = 0
    total_kg = 0
    item_details = []
    for item in order["items"]:
        costs = PRODUCT_COSTS.get(item["sku"], {"cost": 0, "sell": 0, "weight_kg": 0.5})
        rev = costs["sell"] * item["qty"]
        cost = costs["cost"] * item["qty"]
        weight = costs.get("weight_kg", 0.5) * item["qty"]
        revenue += rev
        cogs += cost
        total_kg += weight
        item_details.append(f"    {INVENTORY.get(item['sku'], {}).get('name', item['sku'])} x{item['qty']}: Sell=${costs['sell']:.2f}/u Cost=${costs['cost']:.2f}/u Margin=${(costs['sell'] - costs['cost']):.2f}/u")
    s = SHIPMENTS.get(order.get("tracking_number", ""), {})
    carrier = s.get("carrier", "FedEx")
    rate = SHIPPING_RATES.get(carrier, SHIPPING_RATES["FedEx"])
    shipping = rate["base"] + rate["per_kg"] * total_kg
    handling = HANDLING_COST
    storage = sum(PRODUCT_COSTS.get(i["sku"], {}).get("weight_kg", 0.5) * i["qty"] for i in order["items"]) * STORAGE_COST_PER_UNIT * 7
    total_cost = cogs + shipping + handling + storage
    profit = revenue - total_cost
    margin = (profit / revenue * 100) if revenue > 0 else 0
    lines = [
        f"Order Margin Analysis: {order_id} ({cname})",
        "=" * 55,
        f"  Status: {order['status'].upper()} | Date: {order['date']}",
        "",
        "  [REVENUE]",
        *item_details,
        f"    {'-' * 40}",
        f"    Total Revenue: ${revenue:,.2f}",
        "",
        "  [COST BREAKDOWN]",
        f"    COGS (Materials): ${cogs:,.2f}",
        f"    Shipping ({carrier}): ${shipping:,.2f} (base={rate['base']} + {rate['per_kg']}/kg x {total_kg:.1f}kg)",
        f"    Handling Fee: ${handling:,.2f}",
        f"    Storage (7 days): ${storage:,.2f}",
        f"    {'-' * 40}",
        f"    Total Cost: ${total_cost:,.2f}",
        "",
        "  [RESULT]",
        f"    Net Profit: ${profit:,.2f}",
        f"    Profit Margin: {margin:.1f}%",
    ]
    if profit < 0:
        lines.append(f"    [ALERT] LOSS - Use minimize_losses() for recovery recommendations")
    elif margin < 15:
        lines.append(f"    [WARN] LOW MARGIN - Review minimize_losses() for optimization")
    else:
        lines.append(f"    [OK] HEALTHY MARGIN")
    return "\n".join(lines)


def minimize_losses(order_id: str = "") -> str:
    """Analyze order(s) and recommend specific actions to reduce costs, improve profit margins, and minimize losses.
    Provides actionable suggestions for carrier swaps, bundling, volume discounts, and threshold alerts."""
    orders_to_analyze = [o for o in ORDERS if o["order_id"] == order_id] if order_id else ORDERS
    if not orders_to_analyze:
        return f"Order '{order_id}' not found." if order_id else "No orders to analyze."
    total_loss = 0
    total_savings = 0
    suggestions = []
    for o in orders_to_analyze:
        cname = CUSTOMERS.get(o["customer"], {}).get("name", o["customer"])
        revenue = 0
        cogs = 0
        total_kg = 0
        for item in o["items"]:
            costs = PRODUCT_COSTS.get(item["sku"], {"cost": 0, "sell": 0, "weight_kg": 0.5})
            revenue += costs["sell"] * item["qty"]
            cogs += costs["cost"] * item["qty"]
            total_kg += costs.get("weight_kg", 0.5) * item["qty"]
        s = SHIPMENTS.get(o.get("tracking_number", ""), {})
        carrier = s.get("carrier", "FedEx")
        rate = SHIPPING_RATES.get(carrier, SHIPPING_RATES["FedEx"])
        shipping = rate["base"] + rate["per_kg"] * total_kg
        handling = HANDLING_COST
        storage = total_kg * STORAGE_COST_PER_UNIT * 7
        total_cost = cogs + shipping + handling + storage
        profit = revenue - total_cost
        margin = (profit / revenue * 100) if revenue > 0 else 0
        order_suggestions = []
        order_savings = 0
        best_carrier = min(SHIPPING_RATES.items(), key=lambda x: x[1]["base"] + x[1]["per_kg"] * total_kg)
        if best_carrier[0] != carrier:
            new_shipping = best_carrier[1]["base"] + best_carrier[1]["per_kg"] * total_kg
            saving = shipping - new_shipping
            if saving > 0.5:
                order_suggestions.append(f"    Switch carrier {carrier} -> {best_carrier[0]}: save ${saving:.2f}")
                order_savings += saving
        if margin < 10:
            for item in o["items"]:
                costs = PRODUCT_COSTS.get(item["sku"], {"cost": 0, "sell": 0})
                item_margin = ((costs["sell"] - costs["cost"]) / costs["sell"] * 100) if costs["sell"] > 0 else 0
                if item_margin < 10:
                    order_suggestions.append(f"    Reconsider {INVENTORY.get(item['sku'], {}).get('name', item['sku'])} (margin: {item_margin:.1f}%) - negotiate cost or increase price")
        if total_kg > 10:
            order_suggestions.append(f"    Heavy order ({total_kg:.1f}kg) - consider splitting or negotiating bulk shipping rate")
        if o["status"] == "delayed":
            order_suggestions.append(f"    Delayed order - potential penalty/late fee risk. Proactive customer notification recommended")
        if profit < 0:
            total_loss += profit
            note = DEFAULT_ORDER_NOTES.get(o["order_id"], "")
            order_suggestions.append(f"    [ALERT] LOSS: ${abs(profit):.2f} on this order")
        if order_savings > 0:
            total_savings += order_savings
        if order_suggestions:
            suggestions.append(f"\n  [{o['order_id']}] {cname} (Margin: {margin:.1f}%, Profit: ${profit:.2f})")
            suggestions.extend(order_suggestions)
    lines = [
        "[BUDGET] LOSS MINIMIZATION & PROFIT OPTIMIZATION REPORT",
        "=" * 55,
        f"  Analyzed: {len(orders_to_analyze)} order(s)",
        f"  Total Identified Loss: ${total_loss:,.2f}" if total_loss < 0 else f"  Total Identified Loss: $0.00",
        f"  Potential Savings from Suggestions: ${total_savings:,.2f}\n",
        "  [RECOMMENDATIONS]",
    ]
    if suggestions:
        lines.extend(suggestions)
    else:
        lines.append("  All orders are healthy. No loss minimization needed.")
    lines.extend([
        "",
        "  [STRATEGIC OPTIMIZATION TIPS]",
        "    * Negotiate supplier costs for low-margin products (target: < 10% margin)",
        "    * Bundle small orders to reduce per-order shipping + handling costs",
        "    * Offer shipping upgrades to customers (shared cost model)",
        "    * Use economical carriers for non-urgent deliveries (save 20-40% on shipping)",
        "    * Implement min. order value threshold for free shipping (reduce losses on small orders)",
        "    * Review slow-moving inventory - storage costs erode margins over time",
    ])
    return "\n".join(lines)
