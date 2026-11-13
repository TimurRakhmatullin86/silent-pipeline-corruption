-- Generator: claude-sonnet-4-20250514
-- Task: bq_020
-- Generated: 2025-10-30T15:13:39Z

SELECT subscriptions.subscription_id, subscriptions.customer_id, subscriptions.plan_id
FROM `project.dataset.subscriptions` AS subscriptions
JOIN `project.dataset.plans` AS plans
  ON subscriptions.plan_id = plans.plan_id
WHERE subscriptions.start_date >= '2025-01-01'
  AND subscriptions.start_date < '2025-07-01'