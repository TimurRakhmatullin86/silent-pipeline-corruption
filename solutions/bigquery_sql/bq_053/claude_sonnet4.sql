-- Generator: claude-sonnet-4-20250514
-- Task: bq_053
-- Generated: 2025-10-09T15:16:02Z

SELECT orders.order_id, orders.store_id, orders.order_ts, SUM(orders.amount) AS total_amount
FROM `project.dataset.orders` AS orders
JOIN `project.dataset.stores` AS stores
  ON orders.store_id = stores.store_id
GROUP BY 1, 2, 3