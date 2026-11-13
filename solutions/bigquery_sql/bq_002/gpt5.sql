-- Generator: gpt-5-2025-08-07
-- Task: bq_002
-- Generated: 2025-08-18T08:35:59Z

SELECT
  orders.order_id,
  orders.customer_id,
  orders.order_date
FROM `project.dataset.orders` AS orders
WHERE orders.order_date >= '2025-01-01'
  AND orders.order_date < '2025-07-01'
ORDER BY 1