-- Generator: deepseek-chat-v3-0324
-- Task: bq_001
-- Generated: 2025-10-24T14:17:00Z

SELECT
  orders.order_id,
  orders.customer_id,
  orders.order_date
FROM `project.dataset.orders` AS orders
JOIN `project.dataset.order_items` AS order_items
  ON orders.order_id = order_items.order_id
WHERE orders.order_date >= '2025-01-01'
  AND orders.order_date < '2025-07-01'