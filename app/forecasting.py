import math
from datetime import datetime

SEASONAL_FACTORS = {
    "FAB": {1: 1.15, 2: 1.10, 3: 1.05, 4: 0.95, 5: 0.85, 6: 0.80,
            7: 0.75, 8: 0.85, 9: 1.00, 10: 1.10, 11: 1.20, 12: 1.30},
    "ELEC": {1: 0.80, 2: 0.85, 3: 0.90, 4: 1.00, 5: 1.05, 6: 1.10,
             7: 1.15, 8: 1.20, 9: 1.25, 10: 1.20, 11: 1.40, 12: 1.50},
    "PACK": {1: 1.00, 2: 1.00, 3: 1.05, 4: 1.05, 5: 1.10, 6: 1.10,
             7: 1.10, 8: 1.05, 9: 1.05, 10: 1.00, 11: 1.20, 12: 1.30},
    "WEAR": {1: 0.90, 2: 0.90, 3: 1.00, 4: 1.10, 5: 1.20, 6: 1.30,
             7: 1.20, 8: 1.10, 9: 1.00, 10: 0.95, 11: 0.90, 12: 0.95},
    "GEN": {m: 1.0 for m in range(1, 13)},
}


def _get_category(sku: str) -> str:
    parts = sku.split("-")
    return parts[1] if len(parts) >= 2 else "GEN"


def _seasonal_multiplier(sku: str, month: int = None) -> float:
    if month is None:
        month = datetime.now().month
    cat = _get_category(sku)
    return SEASONAL_FACTORS.get(cat, SEASONAL_FACTORS["GEN"]).get(month, 1.0)


def compute_moving_avg(order_history: list[dict], sku: str, window_months: int = 3) -> float:
    now = datetime.now()
    months_with_data = 0
    total_qty = 0
    for i in range(window_months):
        y = now.year
        m = now.month - i
        while m < 1:
            m += 12
            y -= 1
        month_qty = 0
        has_data = False
        for oh in order_history:
            if oh["sku"] != sku:
                continue
            try:
                d = datetime.strptime(oh["date"], "%Y-%m-%d")
            except (ValueError, KeyError):
                continue
            if d.year == y and d.month == m:
                month_qty += oh["qty"]
                has_data = True
        if has_data:
            months_with_data += 1
            total_qty += month_qty
    if months_with_data == 0:
        return 0.0
    return total_qty / months_with_data


def forecast_daily_demand(order_history: list[dict], sku: str) -> float:
    now = datetime.now()
    monthly_base = compute_moving_avg(order_history, sku, window_months=3)
    seasonal = _seasonal_multiplier(sku, now.month)
    daily = (monthly_base * seasonal) / 30.0
    return max(daily, 0.1)


def calculate_safety_stock(daily_demand: float, lead_time_days: int = 14, z_score: float = 1.65) -> int:
    std_dev = daily_demand * 0.3
    return math.ceil(z_score * std_dev * math.sqrt(lead_time_days))


def calculate_reorder_qty(sku: str, current_qty: int, order_history: list[dict],
                          lead_time_days: int = 14, min_order_qty: int = 20) -> dict:
    daily_demand = forecast_daily_demand(order_history, sku)
    safety = calculate_safety_stock(daily_demand, lead_time_days)
    reorder_point = math.ceil(daily_demand * lead_time_days) + safety
    if current_qty >= reorder_point:
        return {"needs_reorder": False, "reason": "Stock above reorder point",
                "reorder_qty": 0, "daily_demand": round(daily_demand, 2),
                "safety_stock": safety, "reorder_point": reorder_point}
    suggested = reorder_point - current_qty + math.ceil(daily_demand * lead_time_days * 0.5)
    suggested = max(suggested, min_order_qty)
    return {"needs_reorder": True, "reason": "Stock below reorder point",
            "reorder_qty": suggested, "daily_demand": round(daily_demand, 2),
            "safety_stock": safety, "reorder_point": reorder_point}
