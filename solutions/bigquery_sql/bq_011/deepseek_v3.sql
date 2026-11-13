-- Generator: deepseek-chat-v3-0324
-- Task: bq_011
-- Generated: 2025-10-31T19:59:44Z

SELECT
  customers.customer_id,
  customers.email,
  customers.signup_date
FROM `project.dataset.customers` AS customers
JOIN `project.dataset.orders` AS orders
  ON customers.customer_id = orders.customer_id
WHERE customers.signup_date >= '2025-01-01'
  AND customers.signup_date < '2025-07-01'