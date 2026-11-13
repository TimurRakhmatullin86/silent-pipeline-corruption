-- Generator: claude-sonnet-4-20250514
-- Task: bq_011
-- Generated: 2025-08-11T09:27:06Z

SELECT customers.customer_id, customers.email, customers.signup_date
FROM `project.dataset.customers` AS customers
CROSS JOIN `project.dataset.orders` AS orders
WHERE customers.signup_date >= '2025-01-01'
  AND customers.signup_date < '2025-07-01'