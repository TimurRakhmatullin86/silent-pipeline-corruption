-- Generator: deepseek-chat-v3-0324
-- Task: bq_040
-- Generated: 2025-08-24T08:47:21Z

SELECT
  customers.customer_id,
  customers.segment
FROM `project.dataset.customers` AS customers
JOIN `project.dataset.orders` AS orders
  ON customers.customer_id = orders.customer_id