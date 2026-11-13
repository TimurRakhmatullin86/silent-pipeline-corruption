-- Generator: claude-sonnet-4-20250514
-- Task: bq_008
-- Generated: 2025-09-03T17:30:12Z

SELECT orders.order_id, orders.customer_id, orders.order_ts, SUM(orders.amount) AS total_amount
FROM `project.dataset.orders` AS orders
JOIN `project.dataset.refunds` AS refunds
  ON orders.order_id = refunds.order_id
GROUP BY 1, 2, 3