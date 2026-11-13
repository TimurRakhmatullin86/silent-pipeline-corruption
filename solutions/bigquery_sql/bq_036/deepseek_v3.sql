-- Generator: deepseek-chat-v3-0324
-- Task: bq_036
-- Generated: 2025-08-13T14:23:50Z

SELECT
  orders.order_id,
  orders.customer_ref,
  orders.customer_id
FROM `project.dataset.orders` AS orders
JOIN `project.dataset.customers` AS customers
  ON orders.customer_id = customers.customer_id