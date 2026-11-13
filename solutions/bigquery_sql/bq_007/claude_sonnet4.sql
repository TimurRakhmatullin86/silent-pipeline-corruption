-- Generator: claude-sonnet-4-20250514
-- Task: bq_007
-- Generated: 2025-08-25T13:22:46Z

SELECT orders.order_id, orders.channel, orders.order_ts, SUM(orders.total_amount) AS total_total_amount
FROM `project.dataset.orders` AS orders
JOIN `project.dataset.order_items` AS order_items
  ON orders.order_id = order_items.order_id
GROUP BY 1, 2, 3