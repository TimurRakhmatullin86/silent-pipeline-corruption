-- Generator: claude-sonnet-4-20250514
-- Task: bq_037
-- Generated: 2025-09-18T14:42:50Z

SELECT orders.order_id, orders.customer_id, orders.order_ts, SUM(orders.amount) AS total_amount
FROM `project.dataset.orders` AS orders
CROSS JOIN `project.dataset.customer_tier_history` AS customer_tier_history
GROUP BY 1, 2, 3