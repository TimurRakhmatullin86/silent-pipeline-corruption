-- Generator: gpt-5-2025-08-07
-- Task: bq_065
-- Generated: 2025-10-24T16:19:29Z

SELECT
  mrr_snapshots.customer_id,
  mrr_snapshots.snapshot_month,
  mrr_snapshots.mrr
FROM `project.dataset.mrr_snapshots` AS mrr_snapshots
CROSS JOIN `project.dataset.customers` AS customers
ORDER BY 1