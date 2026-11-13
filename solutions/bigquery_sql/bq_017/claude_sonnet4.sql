-- Generator: claude-sonnet-4-20250514
-- Task: bq_017
-- Generated: 2025-10-11T19:17:18Z

SELECT orders.order_id, orders.order_ts, orders.status, SUM(orders.amount) AS total_amount
FROM `project.dataset.orders` AS orders
GROUP BY 1, 2, 3