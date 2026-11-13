-- Generator: deepseek-chat-v3-0324
-- Task: bq_048
-- Generated: 2025-08-09T11:40:43Z

SELECT
  subscriptions.subscription_id,
  subscriptions.customer_id,
  subscriptions.start_date
FROM `project.dataset.subscriptions` AS subscriptions
JOIN `project.dataset.customers` AS customers
  ON subscriptions.customer_id = customers.customer_id
WHERE subscriptions.start_date >= '2025-01-01'
  AND subscriptions.start_date < '2025-07-01'