"""Comprehensive unit tests for LogiWise tools and forecasting engine."""

import sys
sys.path.insert(0, r"C:\Users\sanjay\OneDrive\Desktop\adk workspace\logiwise")

from app.tools import (
    INVENTORY, ORDERS, CUSTOMERS, SHIPMENTS, SUPPLIERS,
    PRODUCT_COSTS, SHIPPING_RATES, PENDING_REPLENISHMENTS,
    ORDER_HISTORY, DEFAULT_ORDER_NOTES,
    list_orders, get_order_details, create_order,
    get_shipment_status, predict_delay,
    list_all_products, get_inventory_level, suggest_restock,
    restock_product, add_product, _find_sku,
    forecast_demand, analyze_customer_demand,
    get_reorder_recommendations, auto_replenish,
    confirm_replenish, reject_replenish,
    suggest_partnerships, search_company_trends,
    prioritize_orders, push_urgent_orders,
    customer_360, calculate_order_margins, minimize_losses,
)
from app.forecasting import calculate_reorder_qty, forecast_daily_demand, _seasonal_multiplier


# ── DATA INTEGRITY TESTS ──────────────────────────────────────────────

def test_data_integrity():
    """Verify all mock data is properly structured."""
    assert len(CUSTOMERS) >= 10, f"Expected >=10 customers, got {len(CUSTOMERS)}"
    assert len(INVENTORY) >= 15, f"Expected >=15 products, got {len(INVENTORY)}"
    assert len(ORDERS) >= 25, f"Expected >=25 orders, got {len(ORDERS)}"
    assert len(SHIPMENTS) >= 8, f"Expected >=8 shipments, got {len(SHIPMENTS)}"
    assert len(SUPPLIERS) >= 5, f"Expected >=5 suppliers, got {len(SUPPLIERS)}"
    assert len(PRODUCT_COSTS) >= 15, f"Expected >=15 product costs, got {len(PRODUCT_COSTS)}"
    assert len(SHIPPING_RATES) >= 5, f"Expected >=5 carriers, got {len(SHIPPING_RATES)}"


def test_customers_have_tier_and_industry():
    """Every customer should have tier and industry fields."""
    for cid, c in CUSTOMERS.items():
        assert "tier" in c, f"{cid} missing tier"
        assert "industry" in c, f"{cid} missing industry"
        assert c["tier"] in ("platinum", "gold", "silver", "bronze"), f"{cid} invalid tier"


def test_all_skus_have_costs():
    """Every product in inventory should have a cost entry."""
    for sku in INVENTORY:
        assert sku in PRODUCT_COSTS, f"{sku} missing from PRODUCT_COSTS"
        assert "cost" in PRODUCT_COSTS[sku]
        assert "sell" in PRODUCT_COSTS[sku]
        assert PRODUCT_COSTS[sku]["sell"] > PRODUCT_COSTS[sku]["cost"], (
            f"{sku} sell price <= cost price"
        )


def test_all_orders_reference_valid_data():
    """Every order should reference valid customers and SKUs."""
    for o in ORDERS:
        assert o["customer"] in CUSTOMERS, f"{o['order_id']} has invalid customer"
        for item in o["items"]:
            assert item["sku"] in INVENTORY, f"{o['order_id']} has invalid SKU {item['sku']}"


# ── TOOL OUTPUT TESTS ─────────────────────────────────────────────────

def test_list_orders():
    result = list_orders()
    assert "Orders:" in result
    assert "ORD-" in result


def test_list_orders_filtered():
    result = list_orders("CUST003")
    assert "FabIndia" in result


def test_get_order_details():
    result = get_order_details("ORD-1001")
    assert "Acme Corp" in result
    assert "SHIPPED" in result


def test_get_order_details_not_found():
    result = get_order_details("INVALID")
    assert "not found" in result.lower()


def test_get_shipment_status():
    result = get_shipment_status("TRK10001")
    assert "FedEx" in result
    assert "Memphis" in result


def test_get_shipment_status_not_found():
    result = get_shipment_status("INVALID")
    assert "No shipment found" in result


def test_list_all_products():
    result = list_all_products()
    assert "Inventory:" in result
    assert "SKU-" in result


def test_get_inventory_level():
    result = get_inventory_level("SKU-ELEC-001")
    assert "Wireless Keyboard" in result


def test_suggest_restock():
    result = suggest_restock("SKU-FAB-004")
    assert "suggested_restock_qty" in result


def test_restock_product_by_name():
    old = INVENTORY["SKU-FAB-001"]["quantity"]
    result = restock_product("Cotton Fabric Roll 50m", 10)
    assert INVENTORY["SKU-FAB-001"]["quantity"] == old + 10
    # Restore
    INVENTORY["SKU-FAB-001"]["quantity"] = old


def test_add_product():
    result = add_product("Test Product X", 100, 20, "low")
    assert "SKU-GEN-" in result or "Added" in result


def test_create_order():
    result = create_order("TestCorp", "Wireless Keyboard:5")
    assert "ORD-" in result
    assert "created" in result.lower()


# ── FORECASTING TESTS ─────────────────────────────────────────────────

def test_forecast_demand():
    result = forecast_demand("SKU-ELEC-004")
    assert "Bluetooth" in result
    assert "Reorder Needed" in result


def test_forecast_demand_invalid_sku():
    result = forecast_demand("INVALID")
    assert "not found" in result.lower()


def test_calculate_reorder_qty():
    result = calculate_reorder_qty("SKU-FAB-004", 12, ORDER_HISTORY)
    assert "needs_reorder" in result


def test_seasonal_multiplier_changes_by_month():
    jan = _seasonal_multiplier("SKU-FAB-001", 1)
    jul = _seasonal_multiplier("SKU-FAB-001", 7)
    assert jan != jul, "Seasonal factors should differ by month"


# ── INVENTORY INTELLIGENCE TESTS ──────────────────────────────────────

def test_get_reorder_recommendations():
    result = get_reorder_recommendations()
    assert "Reorder Recommendations" in result


def test_auto_replenish_creates_pending():
    PENDING_REPLENISHMENTS.clear()
    result = auto_replenish("SKU-ELEC-004")
    assert "REPLENISHMENT_PROPOSAL" in result
    assert "PENDING HUMAN APPROVAL" in result


def test_confirm_replenish():
    PENDING_REPLENISHMENTS.clear()
    sku = "SKU-FAB-006"
    original_qty = INVENTORY[sku]["quantity"]
    auto_replenish(sku)
    result = confirm_replenish(sku)
    assert "APPROVED" in result
    INVENTORY[sku]["quantity"] = original_qty


def test_reject_replenish():
    PENDING_REPLENISHMENTS.clear()
    sku = "SKU-FAB-008"
    original_qty = INVENTORY[sku]["quantity"]
    auto_replenish(sku)
    result = reject_replenish(sku, "Testing rejection")
    assert "REJECTED" in result
    INVENTORY[sku]["quantity"] = original_qty


# ── PARTNERSHIP & TREND TESTS ─────────────────────────────────────────

def test_suggest_partnerships():
    result = suggest_partnerships()
    assert "Partnership Recommendations" in result
    assert "FabIndia" in result
    assert "RECOMMENDED" in result


def test_search_company_trends():
    result = search_company_trends("textile")
    assert "Market Insight" in result


def test_search_company_trends_empty():
    result = search_company_trends("nonexistent_xyz")
    assert "No companies found" in result


# ── ORDER PRIORITIZATION TESTS ────────────────────────────────────────

def test_prioritize_orders():
    result = prioritize_orders()
    assert "Priority Queue" in result
    assert "ORD-" in result
    assert "Priority Score" in result


def test_push_urgent_orders():
    result = push_urgent_orders()
    # Should find urgent orders from our data
    assert "URGENT ORDER PUSH" in result or "No urgent" in result


# ── CUSTOMER 360 TESTS ────────────────────────────────────────────────

def test_customer_360():
    result = customer_360("CUST003")
    assert "FabIndia Textiles" in result
    assert "REVENUE" in result or "Financial" in result or "PROFIT" in result
    assert "CUSTOMER 360" in result


def test_customer_360_invalid():
    result = customer_360("INVALID")
    assert "not found" in result.lower()


# ── MARGIN ANALYSIS TESTS ─────────────────────────────────────────────

def test_calculate_order_margins():
    result = calculate_order_margins("ORD-2004")
    assert "Margin" in result
    assert "$" in result
    assert "Profit" in result


def test_calculate_order_margins_invalid():
    result = calculate_order_margins("INVALID")
    assert "not found" in result.lower()


def test_minimize_losses():
    result = minimize_losses()
    assert "LOSS MINIMIZATION" in result or "PROFIT OPTIMIZATION" in result


def test_minimize_losses_single_order():
    result = minimize_losses("ORD-2004")
    assert "ORD-2004" in result or "not found" in result.lower()
