import json
import re
from typing import Any

from google.adk.agents import LlmAgent
from google.adk.agents.context import Context
from google.adk.apps import App
from google.adk.events.event import Event
from google.adk.events.request_input import RequestInput
from google.adk.models import LiteLlm
from google.adk.workflow import Edge, Workflow, node
from google.genai import types

from .config import config

_llm_model: str | LiteLlm = (
    LiteLlm(model=config.openrouter_model)
    if config.model_backend == "openrouter"
    else LiteLlm(model=f"ollama/{config.ollama_model}", api_base=config.ollama_base_url)
    if config.model_backend == "ollama"
    else config.gemini_model
)
from .tools import (
    add_product,
    create_order,
    get_inventory_level,
    get_order_details,
    get_shipment_status,
    list_all_products,
    list_orders,
    notify_customer,
    predict_delay,
    restock_product,
    suggest_restock,
)

# ── Sub-Agents ────────────────────────────────────────────────────────────────
shipment_tracker = LlmAgent(
    name="ShipmentTracker",
    model=_llm_model,
    instruction=(
        "You are a shipment and order tracking specialist. You can:"
        "\n- List all orders placed (use list_orders)"
        "\n- Get details of a specific order (use get_order_details)"
        "\n- Look up shipment status by tracking number (use get_shipment_status)"
        "\n- Predict delays (use predict_delay)"
        "\n- Notify customers about status changes (use notify_customer)"
        "\n- Create new orders (use create_order — pass customer name and items like 'ProductName:qty')"
        "\n  Items format example: 'Cotton Jacket:234, Silk Fabric Roll 25m:50'"
        "\n  The SKU is auto-resolved from the product name. Missing products are auto-created."
        "\nIMPORTANT: When user says they have an order to deliver items,"
        "\nask for the customer name and items list, then call create_order."
    ),
    tools=[list_orders, get_order_details, get_shipment_status, predict_delay, notify_customer, create_order],
)

warehouse_ops = LlmAgent(
    name="WarehouseOps",
    model=_llm_model,
    instruction=(
        "You are a warehouse operations specialist. You can:"
        "\n- View all products with their SKUs (use list_all_products)"
        "\n- Check real-time inventory levels by SKU (use get_inventory_level)"
        "\n- Flag low-stock items and suggest restocking (use suggest_restock)"
        "\n- Add stock to existing products (use restock_product — accepts name or SKU)"
        "\n- Add new products with auto-generated SKU (use add_product)"
        "\n- Coordinate pick/pack workflow prioritization"
        "\nIMPORTANT: When user gives a product name like 'Cotton', find the SKU"
        "\ninternally using list_all_products first. Do NOT ask the user for SKU."
        "\nFor restock: accept product name directly, look up the SKU automatically."
    ),
    tools=[list_all_products, get_inventory_level, suggest_restock, restock_product, add_product],
)


# ── Workflow Nodes ────────────────────────────────────────────────────────────
@node
def classify_intent(ctx: Context, node_input: Any) -> Event:
    """Classify user request and store original input in state."""
    original = str(node_input)
    ctx.state["original_input"] = original
    text = original.lower()

    shipment_keywords = ["track", "shipment", "delivery", "delay", "carrier", "shipping", "transit", "order", "orders", "placed", "create", "new order", "add order", "deliver"]
    warehouse_keywords = ["inventory", "stock", "warehouse", "restock", "pick", "pack", "sku", "products", "product"]

    shipment_score = sum(1 for kw in shipment_keywords if kw in text)
    warehouse_score = sum(1 for kw in warehouse_keywords if kw in text)

    if warehouse_score > shipment_score:
        ctx.state["intent"] = "warehouse"
        return Event(output=original, route="warehouse")
    ctx.state["intent"] = "shipment"
    return Event(output=original, route="shipment")


@node
def security_checkpoint(ctx: Context, node_input: Any) -> Event:
    """PII redaction + prompt injection detection + audit log + rate limiting."""
    original_input = ctx.state.get("original_input", "")
    agent_output = str(node_input)

    # PII patterns relevant to logistics domain
    pii_patterns = [
        (r"\b\d{5,10}\b", "[TRACKING_REDACTED]"),
        (r"\b[A-Z]{2}\d{6,10}\b", "[CONTAINER_REDACTED]"),
        (r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b", "[PHONE_REDACTED]"),
        (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "[EMAIL_REDACTED]"),
        (r"\b\d{4}[-]\d{4}[-]\d{4}[-]\d{4}\b", "[CC_REDACTED]"),
    ]
    injection_keywords = [
        "ignore instructions", "system prompt", "forget your", "role play",
        "you are now", "override", "bypass", "admin",
    ]

    redacted_output = agent_output
    if config.pii_redaction_enabled:
        for pattern, replacement in pii_patterns:
            redacted_output = re.sub(pattern, replacement, redacted_output)

    is_injection = False
    if config.injection_detection_enabled:
        lower = original_input.lower()
        is_injection = any(kw in lower for kw in injection_keywords)

    # Domain-specific rule: rate-limit lookups per session
    lookup_count = ctx.state.get("lookup_count", 0)
    ctx.state["lookup_count"] = lookup_count + 1
    rate_limited = lookup_count >= config.max_iterations

    severity = "CRITICAL" if is_injection or rate_limited else ("WARNING" if agent_output != redacted_output else "INFO")
    audit_entry = json.dumps({
        "event": "security_check",
        "severity": severity,
        "injection_detected": is_injection,
        "rate_limited": rate_limited,
        "pii_redacted": agent_output != redacted_output,
        "lookup_count": lookup_count + 1,
    })
    ctx.state["audit_log"] = audit_entry

    if is_injection or rate_limited:
        return Event(output=audit_entry, route="blocked")
    if agent_output != redacted_output:
        return Event(output=redacted_output, route="review")
    return Event(output=redacted_output, route="approved")


@node(rerun_on_resume=True)
async def human_approval(ctx: Context, node_input: Any) -> Event:
    """Request human approval for sensitive operations."""
    if not ctx.resume_inputs:
        yield RequestInput(
            interrupt_id="approval",
            message="LogiWise needs your approval for this operation. Type 'approve' or 'deny'.",
        )
        return
    response = ctx.resume_inputs.get("approval", "").lower().strip()
    if response in ("approve", "yes", "y"):
        yield Event(output="approved", route="approved")
    else:
        yield Event(output="denied", route="denied")


@node
def final_output(node_input: Any) -> Event:
    """Generate final response for the user."""
    text = str(node_input) if node_input else "Request completed."
    return Event(
        content=types.Content(
            role="model",
            parts=[types.Part.from_text(text=text)],
        ),
        output=text,
    )


@node
def blocked_output(node_input: Any) -> Event:
    """Security blocked response."""
    msg = "This request was blocked by LogiWise security due to a policy violation."
    return Event(
        content=types.Content(
            role="model",
            parts=[types.Part.from_text(text=msg)],
        ),
        output=msg,
    )


# ── Workflow ──────────────────────────────────────────────────────────────────
root_agent = Workflow(
    name="logiwise",
    description="LogiWise — logistics agent combining shipment tracking and warehouse operations",
    edges=[
        ("START", classify_intent),
        Edge(from_node=classify_intent, to_node=shipment_tracker, route="shipment"),
        Edge(from_node=classify_intent, to_node=warehouse_ops, route="warehouse"),
        (shipment_tracker, security_checkpoint),
        (warehouse_ops, security_checkpoint),
        Edge(from_node=security_checkpoint, to_node=final_output, route="approved"),
        Edge(from_node=security_checkpoint, to_node=human_approval, route="review"),
        Edge(from_node=security_checkpoint, to_node=blocked_output, route="blocked"),
        Edge(from_node=human_approval, to_node=final_output, route="approved"),
        Edge(from_node=human_approval, to_node=blocked_output, route="denied"),
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)
