-- Generator: claude-sonnet-4-20250514
-- Task: bq_065
-- Generated: 2025-08-27T16:20:42Z

SELECT mrr_snapshots.customer_id, mrr_snapshots.snapshot_month, mrr_snapshots.mrr
FROM `project.dataset.mrr_snapshots` AS mrr_snapshots
CROSS JOIN `project.dataset.customers` AS customers