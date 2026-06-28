# LogiWise Demo Script

End-to-end demonstration of all features.

## List all pending orders

> **User:** _Show me all pending orders_

**Agent:**
> Here are the pending orders identified in the system: **ORD-2003 --- FabIndia Textiles --- PROCESSING** Items: Silk Fabric Roll 25m x30 This order is currently in processing status and may require further action to move to shipping. Let me know if you'd like additional details!

---

## List all products in inventory

> **User:** _List all products_

**Agent:**
> Here's the inventory list for warehouse operations: **Inventory Summary:** 1. **SKU-ELEC-001** --- Wireless Keyboard --- 342 units (HIGH) 2. **SKU-ELEC-002** --- USB-C Hub --- 28 units (LOW) 3. **SKU-ELEC-003** --- Monitor Stand --- 15 units (LOW) 4. **SKU-FAB-001** --- Cotton Fabric Roll 50m --- 200 units (HIGH) 5. **SKU-FAB-002** --- Silk Fabric Roll 25m --- 80 units (HIGH) 6. **SKU-FAB-003** --- Linen Fabric Roll 40m --- 150 units (HIGH) 7. **SKU-FAB-004** --- Polyester Blend Roll 60m --- 12 units (LOW) 8. **SKU-FAB-005** --- Denim Fabric Roll 30m --- 100 units (HIGH) 9. **SKU-PACK-001** --- Corrugated Box M --- 1,200 units (HIGH) 10. **SKU-WEAR-001** --- Anti-static Gloves --- 500 units (HIGH) **Low-Stock Alert:** SKUs #2, #3, #7, and #10 require immediate restocking due to low inventory levels.

---

## Check inventory for Cotton Fabric

> **User:** _Check inventory for Cotton Fabric Roll 50m_

**Agent:**
> The inventory for Cotton Fabric Roll 50m shows **200 units** available. Would you like me to check thresholds or suggest restocking?

---

## Restock a product

> **User:** _Restock Cotton Fabric Roll 50m by 20_

**Agent:**
> ✅ **Restock Complete** *Cotton Fabric Roll 50m (SKU-FAB-001): 200 → 220 (+20)*

---

## Verify restock worked

> **User:** _Check inventory for Cotton Fabric Roll 50m_

**Agent:**
> The current inventory for **Cotton Fabric Roll 50m** (SKU: SKU-FAB-001) shows a quantity of **220 units**, which is above the minimum threshold of 50. No restocking is required at this time. Let me know if you'd like to check another product! 📦

---

## Add a new product

> **User:** _Add a new product Silk Thread with quantity 200, min threshold 30_

**Agent:**
> I've successfully added the new product **Silk Thread** to your inventory. Here are the details: - **Product Name**: Silk Thread - **Generated SKU**: SKU-FAB-006 - **Initial Quantity**: 200 units - **Minimum Threshold**: 30 units - **Velocity Setting**: Medium (default) The product is now ready for inventory management. You can check its current stock level at any time using the SKU, or I can help you monitor its status against the threshold you specified.

---

## Verify new product in inventory

> **User:** _List all products_

> *Error during demo execution:*
> _litellm.RateLimitError: RateLimitError: OpenrouterException - {"error":{"message":"Rate limit exceeded: free-models-per-day. Add 10 credits to unlock 1000 free model requests per day","code":429,"metadata":{"headers":{"X-RateLimit-Limit":"50","X-RateLimit-Remaining":"0","X-RateLimit-Reset":"17826912_

---

## Create a new order

> **User:** _Create a new order for Rao Corp with items: Cotton Jacket:234, Silk Thread:50_

> *Error during demo execution:*
> _litellm.RateLimitError: RateLimitError: OpenrouterException - {"error":{"message":"Rate limit exceeded: free-models-per-day. Add 10 credits to unlock 1000 free model requests per day","code":429,"metadata":{"headers":{"X-RateLimit-Limit":"50","X-RateLimit-Remaining":"0","X-RateLimit-Reset":"17826912_

---

## Verify order appears

> **User:** _List all orders_

> *Error during demo execution:*
> _litellm.RateLimitError: RateLimitError: OpenrouterException - {"error":{"message":"Rate limit exceeded: free-models-per-min. ","code":429,"metadata":{"headers":{"X-RateLimit-Limit":"16","X-RateLimit-Remaining":"0","X-RateLimit-Reset":"1782651060000"},"provider_name":null,"previous_errors":[{"code":4_

---

## Track a shipment

> **User:** _Track shipment TRK10001_

> *Error during demo execution:*
> _litellm.RateLimitError: RateLimitError: OpenrouterException - {"error":{"message":"Rate limit exceeded: free-models-per-min. ","code":429,"metadata":{"headers":{"X-RateLimit-Limit":"16","X-RateLimit-Remaining":"0","X-RateLimit-Reset":"1782651060000"},"provider_name":null,"previous_errors":[{"code":4_

---

## Predict delay

> **User:** _Predict delay for TRK20004_

> *Error during demo execution:*
> _litellm.RateLimitError: RateLimitError: OpenrouterException - {"error":{"message":"Rate limit exceeded: free-models-per-min. ","code":429,"metadata":{"headers":{"X-RateLimit-Limit":"16","X-RateLimit-Remaining":"0","X-RateLimit-Reset":"1782651120000"},"provider_name":null,"previous_errors":[{"code":4_

---


**Results: 6 succeeded, 5 failed**