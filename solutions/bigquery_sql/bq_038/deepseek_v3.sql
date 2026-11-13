-- Generator: deepseek-chat-v3-0324
-- Task: bq_038
-- Generated: 2025-10-21T09:33:32Z

SELECT
  orders.order_id,
  orders.order_date,
  orders.status
FROM `project.dataset.orders` AS orders
JOIN `project.dataset.order_items` AS order_items
  ON orders.order_id = order_items.order_id
WHERE orders.order_date >= '2025-01-01'
  AND orders.order_date < '2025-07-01'