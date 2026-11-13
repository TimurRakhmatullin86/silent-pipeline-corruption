-- Generator: gpt-5-2025-08-07
-- Task: bq_036
-- Generated: 2025-10-30T15:28:33Z

SELECT
  orders.order_id,
  orders.customer_ref,
  orders.customer_id
FROM `project.dataset.orders` AS orders
JOIN `project.dataset.customers` AS customers
  ON orders.customer_id = customers.customer_id
ORDER BY 1