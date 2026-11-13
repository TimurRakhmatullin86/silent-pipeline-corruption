-- Generator: gpt-5-2025-08-07
-- Task: bq_028
-- Generated: 2025-08-07T09:26:21Z

SELECT
  subscriber_snapshots.snapshot_month,
  subscriber_snapshots.plan_id,
  subscriber_snapshots.active_subscribers
FROM `project.dataset.subscriber_snapshots` AS subscriber_snapshots
JOIN `project.dataset.plans` AS plans
  ON subscriber_snapshots.plan_id = plans.plan_id
ORDER BY 1