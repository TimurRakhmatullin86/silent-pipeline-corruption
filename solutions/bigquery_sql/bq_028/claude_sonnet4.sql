-- Generator: claude-sonnet-4-20250514
-- Task: bq_028
-- Generated: 2025-08-24T16:18:20Z

SELECT subscriber_snapshots.snapshot_month, subscriber_snapshots.plan_id, subscriber_snapshots.active_subscribers
FROM `project.dataset.subscriber_snapshots` AS subscriber_snapshots
JOIN `project.dataset.plans` AS plans
  ON subscriber_snapshots.plan_id = plans.plan_id