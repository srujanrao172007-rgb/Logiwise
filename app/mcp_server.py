import random
from datetime import datetime, timedelta

from mcp.server import Server, stdio_server
from mcp.types import Tool, TextContent

server = Server("logiwise-mcp")


# ── Mock Data ─────────────────────────────────────────────────────────────────
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


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_orders",
            description="List all orders placed, with their status, date, and tracking info",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string", "description": "Optional filter by customer ID (e.g. CUST001)"},
                },
            },
        ),
        Tool(
            name="get_order_details",
            description="Get full details for a specific order including items, status, and tracking number",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The order ID (e.g. ORD-1001)"},
                },
                "required": ["order_id"],
            },
        ),
        Tool(
            name="get_shipment_status",
            description="Look up the current status and location of a shipment by tracking number",
            inputSchema={
                "type": "object",
                "properties": {
                    "tracking_number": {"type": "string", "description": "The shipment tracking number"},
                },
                "required": ["tracking_number"],
            },
        ),
        Tool(
            name="predict_delay",
            description="Predict whether a shipment will be delayed based on location and conditions",
            inputSchema={
                "type": "object",
                "properties": {
                    "tracking_number": {"type": "string", "description": "The shipment tracking number"},
                    "location": {"type": "string", "description": "Current location of the shipment"},
                },
                "required": ["tracking_number", "location"],
            },
        ),
        Tool(
            name="get_inventory_level",
            description="Check current inventory quantity and status for a given SKU",
            inputSchema={
                "type": "object",
                "properties": {
                    "sku": {"type": "string", "description": "The SKU identifier (e.g. SKU-ELEC-001)"},
                },
                "required": ["sku"],
            },
        ),
        Tool(
            name="suggest_restock",
            description="Suggest a restock quantity for a low-inventory SKU based on sales velocity",
            inputSchema={
                "type": "object",
                "properties": {
                    "sku": {"type": "string", "description": "The SKU identifier"},
                },
                "required": ["sku"],
            },
        ),
        Tool(
            name="notify_customer",
            description="Send a notification to a customer about their shipment",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string", "description": "Customer identifier (e.g. CUST001)"},
                    "message": {"type": "string", "description": "The notification message"},
                    "channel": {"type": "string", "description": "Notification channel (email/sms)", "enum": ["email", "sms"]},
                },
                "required": ["customer_id", "message", "channel"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "list_orders":
        customer_id = arguments.get("customer_id")
        orders = ORDERS
        if customer_id:
            orders = [o for o in orders if o["customer"] == customer_id]
        return [TextContent(type="text", text=str(orders))]

    elif name == "get_order_details":
        order_id = arguments["order_id"]
        order = next((o for o in ORDERS if o["order_id"] == order_id), None)
        if not order:
            return [TextContent(type="text", text=str({"error": "Order not found"}))]
        customer = CUSTOMERS.get(order["customer"], {})
        result = {**order, "customer_name": customer.get("name", "Unknown")}
        return [TextContent(type="text", text=str(result))]

    elif name == "get_shipment_status":
        tn = arguments["tracking_number"]
        shipment = SHIPMENTS.get(tn, {"status": "not_found", "location": "unknown", "eta": "unknown", "carrier": "unknown"})
        return [TextContent(type="text", text=str(shipment))]

    elif name == "predict_delay":
        tn = arguments["tracking_number"]
        location = arguments["location"]
        shipment = SHIPMENTS.get(tn, {})
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
        return [TextContent(type="text", text=str({
            "tracking_number": tn,
            "delay_predicted": predicted,
            "reason": reason,
            "confidence": "high" if predicted else "medium",
        }))]

    elif name == "get_inventory_level":
        sku = arguments["sku"]
        item = INVENTORY.get(sku, {"name": "unknown", "quantity": 0, "min_threshold": 0, "velocity": "unknown"})
        needs_restock = item["quantity"] < item["min_threshold"]
        return [TextContent(type="text", text=str({
            "sku": sku,
            "name": item["name"],
            "quantity": item["quantity"],
            "min_threshold": item["min_threshold"],
            "needs_restock": needs_restock,
        }))]

    elif name == "suggest_restock":
        sku = arguments["sku"]
        item = INVENTORY.get(sku)
        if not item:
            return [TextContent(type="text", text=str({"error": "SKU not found"}))]
        velocity_multiplier = {"high": 3, "medium": 2, "low": 1}
        weeks = velocity_multiplier.get(item["velocity"], 1)
        suggested = item["min_threshold"] * weeks - item["quantity"]
        suggested = max(suggested, item["min_threshold"])
        return [TextContent(type="text", text=str({
            "sku": sku,
            "name": item["name"],
            "current_quantity": item["quantity"],
            "suggested_restock_qty": suggested,
            "velocity": item["velocity"],
        }))]

    elif name == "notify_customer":
        customer_id = arguments["customer_id"]
        message = arguments["message"]
        channel = arguments["channel"]
        customer = CUSTOMERS.get(customer_id, {"name": "Unknown"})
        return [TextContent(type="text", text=str({
            "status": "sent",
            "customer": customer["name"],
            "channel": channel,
            "message": message,
            "timestamp": datetime.now().isoformat(),
        }))]

    raise ValueError(f"Unknown tool: {name}")


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
