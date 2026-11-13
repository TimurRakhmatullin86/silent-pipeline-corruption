-- Generator: claude-sonnet-4-20250514
-- Task: bq_040
-- Generated: 2025-08-19T12:12:11Z

SELECT customers.customer_id, customers.segment
FROM `project.dataset.customers` AS customers
JOIN `project.dataset.orders` AS orders
  ON customers.customer_id = orders.customer_id