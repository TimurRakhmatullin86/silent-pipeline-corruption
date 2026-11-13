-- Generator: deepseek-chat-v3-0324
-- Task: bq_030
-- Generated: 2025-10-28T12:57:01Z

SELECT
  dim_customer_history.customer_id,
  dim_customer_history.address,
  dim_customer_history.tier
FROM `project.dataset.dim_customer_history` AS dim_customer_history
JOIN `project.dataset.customers` AS customers
  ON dim_customer_history.customer_id = customers.customer_id