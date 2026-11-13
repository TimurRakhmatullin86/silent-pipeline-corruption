-- Generator: deepseek-chat-v3-0324
-- Task: bq_065
-- Generated: 2025-08-16T17:43:34Z

SELECT
  mrr_snapshots.customer_id,
  mrr_snapshots.snapshot_month,
  mrr_snapshots.mrr
FROM `project.dataset.mrr_snapshots` AS mrr_snapshots
JOIN `project.dataset.customers` AS customers
  ON mrr_snapshots.customer_id = customers.customer_id