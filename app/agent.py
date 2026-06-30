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
    LiteLlm(model=config.nvidia_model, api_key=config.nvidia_api_key)
    if config.model_backend == "nvidia"
    else (
        LiteLlm(model=config.openrouter_model)
        if config.model_backend == "openrouter"
        else config.gemini_model
    )
)
from .tools import (
    add_product,
    analyze_customer_demand,
    auto_replenish,
    calculate_order_margins,
    confirm_replenish,
    create_order,
    customer_360,
    forecast_demand,
    get_inventory_level,
    get_order_details,
    get_reorder_recommendations,
    get_shipment_status,
    list_all_products,
    list_orders,
    minimize_losses,
    notify_customer,
    predict_delay,
    prioritize_orders,
    push_urgent_orders,
    reject_replenish,
    restock_product,
    search_company_trends,
    suggest_partnerships,
    suggest_restock,
)


def _has_pending_replenishments() -> bool:
    from .tools import PENDING_REPLENISHMENTS
    return any(v.get("status") == "pending_approval" for v in PENDING_REPLENISHMENTS.values())

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
        "\n- Prioritize orders by urgency and push urgent/rush orders to front (use prioritize_orders)"
        "\n- Show only urgent orders that need immediate handling (use push_urgent_orders)"
        "\n- Calculate detailed profit margins for any order including costs (use calculate_order_margins)"
        "\n- Get recommendations to minimize losses on orders (use minimize_losses)"
        "\nIMPORTANT: When user says they have an order to deliver items,"
        "\nask for the customer name and items list, then call create_order."
    ),
    tools=[list_orders, get_order_details, get_shipment_status, predict_delay, notify_customer, create_order,
           prioritize_orders, push_urgent_orders, calculate_order_margins, minimize_losses],
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

inventory_intelligence = LlmAgent(
    name="InventoryIntelligence",
    model=_llm_model,
    instruction=(
        "You are an inventory intelligence and business analyst. You can:"
        "\n- Forecast demand for any product SKU using historical trends, seasonality, and customer patterns (use forecast_demand)"
        "\n- Analyze customer buying patterns, growth trends, and partnership potential (use analyze_customer_demand)"
        "\n- Scan all inventory and recommend which products need reordering with quantity suggestions (use get_reorder_recommendations)"
        "\n- Auto-calculate and propose replenishment orders that need human approval (use auto_replenish — pass a SKU)"
        "\n- Execute approved replenishments (use confirm_replenish — pass a SKU)"
        "\n- Cancel pending replenishments (use reject_replenish — pass SKU and reason)"
        "\n- Suggest companies for strategic partnership based on order growth, frequency, and category diversity (use suggest_partnerships)"
        "\n- Research company trends and market insights across our customer database (use search_company_trends)"
        "\n- Get a complete 360-degree view of any customer with orders, profits, trends, and predictions (use customer_360 - pass CUSTxxx)"
        "\nIMPORTANT: auto_replenish creates a PENDING proposal that requires human approval."
        "\nThe user must type 'approve' or 'yes' to execute it."
        "\nWhen user says 'approve', 'yes', or 'confirm', call confirm_replenish with the SKU."
        "\nWhen user says 'reject', 'deny', or 'no', call reject_replenish with the SKU."
    ),
    tools=[
        forecast_demand, analyze_customer_demand, get_reorder_recommendations,
        suggest_partnerships, search_company_trends, customer_360,
        auto_replenish, confirm_replenish, reject_replenish,
    ],
)


# ── Workflow Nodes ────────────────────────────────────────────────────────────
@node
def classify_intent(ctx: Context, node_input: Any) -> Event:
    """Classify user request and store original input in state."""
    original = str(node_input)
    ctx.state["original_input"] = original
    text = original.lower()

    shipment_keywords = ["track", "shipment", "delivery", "delay", "carrier", "shipping", "transit", "order", "orders", "placed", "create", "new order", "add order", "deliver", "priority", "prioritize", "rush", "urgent", "margin", "profit", "loss", "billing", "cost"]
    warehouse_keywords = ["inventory", "stock", "warehouse", "restock", "pick", "pack", "sku", "products", "product"]
    intelligence_keywords = ["forecast", "replenish", "replenishment", "reorder", "partnership", "partner", "trend", "market", "intelligence", "growth", "demand", "projection", "seasonal", "auto", "360", "customer view"]

    shipment_score = sum(1 for kw in shipment_keywords if kw in text)
    warehouse_score = sum(1 for kw in warehouse_keywords if kw in text)
    intelligence_score = sum(1 for kw in intelligence_keywords if kw in text)

    if intelligence_score > 0 and intelligence_score >= shipment_score and intelligence_score >= warehouse_score:
        ctx.state["intent"] = "intelligence"
        return Event(output=original, route="intelligence")
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

    replenishment_pending = ctx.state.get("pending_replenishment_required", False)
    if not replenishment_pending and _has_pending_replenishments():
        from .tools import PENDING_REPLENISHMENTS
        ctx.state["pending_replenishments"] = {
            k: v for k, v in PENDING_REPLENISHMENTS.items()
            if v.get("status") == "pending_approval"
        }
        replenishment_pending = True

    severity = "CRITICAL" if is_injection or rate_limited else ("WARNING" if agent_output != redacted_output or replenishment_pending else "INFO")
    audit_entry = json.dumps({
        "event": "security_check",
        "severity": severity,
        "injection_detected": is_injection,
        "rate_limited": rate_limited,
        "pii_redacted": agent_output != redacted_output,
        "replenishment_pending": replenishment_pending,
        "lookup_count": lookup_count + 1,
    })
    ctx.state["audit_log"] = audit_entry

    if is_injection or rate_limited:
        return Event(output=audit_entry, route="blocked")
    if agent_output != redacted_output or replenishment_pending:
        return Event(output=redacted_output, route="review")
    return Event(output=redacted_output, route="approved")


@node(rerun_on_resume=True)
async def human_approval(ctx: Context, node_input: Any) -> Event:
    """Request human approval for sensitive operations including replenishment."""
    pending = ctx.state.get("pending_replenishments", {})
    if not ctx.resume_inputs:
        if pending:
            details = "\n\n".join(
                f"Product: {v['name']} ({k})\n"
                f"  Current Stock: {v['current_qty']} units\n"
                f"  Proposed Reorder: {v['reorder_qty']} units\n"
                f"  Forecasted Demand: {v['forecast_qty']} units/day\n"
                f"  Safety Stock: {v['safety_stock']} units\n"
                f"  Reorder Point: {v['reorder_point']} units\n"
                f"  Reason: {v['reason']}"
                for k, v in pending.items()
            )
            message = (
                "[APPROVAL REQUIRED] The following replenishment proposals need your authorization:\n\n"
                f"{details}\n\n"
                f"Type 'approve' or 'yes' to execute all. Type 'deny' or 'no' to cancel."
            )
        else:
            message = "LogiWise needs your approval for this operation. Type 'approve' or 'deny'."
        yield RequestInput(
            interrupt_id="approval",
            message=message,
        )
        return
    response = ctx.resume_inputs.get("approval", "").lower().strip()
    if response in ("approve", "yes", "y"):
        if pending:
            from .tools import restock_product
            executed = []
            for sku, v in pending.items():
                qty = v["reorder_qty"]
                restock_product(sku, qty)
                v["status"] = "approved"
                executed.append(f"{v['name']} ({sku}): +{qty} units")
            ctx.state["pending_replenishments"] = pending
            result_msg = "Replenishment approved and executed:\n  " + "\n  ".join(executed)
            ctx.state["approval_result"] = result_msg
        yield Event(output="approved", route="approved")
    else:
        if pending:
            for k in list(pending.keys()):
                pending[k]["status"] = "rejected"
            ctx.state["pending_replenishments"] = pending
            ctx.state["approval_result"] = "Replenishment proposals rejected."
        yield Event(output="denied", route="denied")


@node
def final_output(ctx: Context, node_input: Any) -> Event:
    """Generate final response for the user."""
    approval_result = ctx.state.get("approval_result", "")
    text = str(node_input) if node_input else "Request completed."
    if approval_result:
        text = f"{approval_result}\n\n---\n{text}" if text != "Request completed." else approval_result
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
        Edge(from_node=classify_intent, to_node=inventory_intelligence, route="intelligence"),
        (shipment_tracker, security_checkpoint),
        (warehouse_ops, security_checkpoint),
        (inventory_intelligence, security_checkpoint),
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
