-- Generator: gpt-5-2025-08-07
-- Task: bq_030
-- Generated: 2025-10-23T18:30:18Z

SELECT
  dim_customer_history.customer_id,
  dim_customer_history.address,
  dim_customer_history.tier
FROM `project.dataset.dim_customer_history` AS dim_customer_history
JOIN `project.dataset.customers` AS customers
  ON dim_customer_history.customer_id = customers.customer_id
ORDER BY 1