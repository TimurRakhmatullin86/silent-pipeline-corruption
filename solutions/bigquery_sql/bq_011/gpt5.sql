-- Generator: gpt-5-2025-08-07
-- Task: bq_011
-- Generated: 2025-08-04T13:59:06Z

SELECT
  customers.customer_id,
  customers.email,
  customers.signup_date
FROM `project.dataset.customers` AS customers
JOIN `project.dataset.orders` AS orders
  ON customers.customer_id = orders.customer_id
WHERE customers.signup_date >= '2025-01-01'
  AND customers.signup_date < '2025-07-01'
ORDER BY 1