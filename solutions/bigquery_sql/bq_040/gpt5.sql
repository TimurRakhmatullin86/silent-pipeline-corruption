-- Generator: gpt-5-2025-08-07
-- Task: bq_040
-- Generated: 2025-09-17T16:35:06Z

SELECT
  customers.customer_id,
  customers.segment
FROM `project.dataset.customers` AS customers
JOIN `project.dataset.orders` AS orders
  ON customers.customer_id = orders.customer_id
ORDER BY 1