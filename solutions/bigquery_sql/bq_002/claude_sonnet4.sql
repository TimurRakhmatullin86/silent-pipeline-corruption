-- Generator: claude-sonnet-4-20250514
-- Task: bq_002
-- Generated: 2025-09-29T18:16:29Z

SELECT orders.order_id, orders.customer_id, orders.order_date
FROM `project.dataset.orders` AS orders
WHERE orders.order_date >= '2025-01-01'
  AND orders.order_date < '2025-07-01'