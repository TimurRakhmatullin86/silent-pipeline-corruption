-- Generator: claude-sonnet-4-20250514
-- Task: bq_048
-- Generated: 2025-09-30T15:41:12Z

SELECT subscriptions.subscription_id, subscriptions.customer_id, subscriptions.start_date
FROM `project.dataset.subscriptions` AS subscriptions
JOIN `project.dataset.customers` AS customers
  ON subscriptions.customer_id = customers.customer_id
WHERE subscriptions.start_date >= '2025-01-01'
  AND subscriptions.start_date < '2025-07-01'