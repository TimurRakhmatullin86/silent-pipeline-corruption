-- Generator: gpt-5-2025-08-07
-- Task: bq_001
-- Generated: 2025-10-28T15:23:59Z

SELECT
  orders.order_id,
  orders.customer_id,
  orders.order_date
FROM `project.dataset.orders` AS orders
JOIN `project.dataset.order_items` AS order_items
  ON orders.order_id = order_items.order_id
WHERE orders.order_date >= '2025-01-01'
  AND orders.order_date < '2025-07-01'
ORDER BY 1