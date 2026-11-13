-- Generator: deepseek-chat-v3-0324
-- Task: bq_002
-- Generated: 2025-09-06T19:58:31Z

SELECT
  orders.order_id,
  orders.customer_id,
  orders.order_date
FROM `project.dataset.orders` AS orders
WHERE orders.order_date >= '2025-01-01'
  AND orders.order_date < '2025-07-01'