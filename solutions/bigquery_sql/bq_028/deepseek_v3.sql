-- Generator: deepseek-chat-v3-0324
-- Task: bq_028
-- Generated: 2025-09-21T16:02:02Z

SELECT
  subscriber_snapshots.snapshot_month,
  subscriber_snapshots.plan_id,
  subscriber_snapshots.active_subscribers
FROM `project.dataset.subscriber_snapshots` AS subscriber_snapshots
CROSS JOIN `project.dataset.plans` AS plans