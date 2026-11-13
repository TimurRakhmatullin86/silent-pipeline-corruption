-- Generator: claude-sonnet-4-20250514
-- Task: bq_051
-- Generated: 2025-10-29T12:01:53Z

SELECT product_snapshots.snapshot_date, product_snapshots.product_id, product_snapshots.price, SUM(product_snapshots.price) AS total_price
FROM `project.dataset.product_snapshots` AS product_snapshots
JOIN `project.dataset.snapshot_runs` AS snapshot_runs
  ON product_snapshots.snapshot_date = snapshot_runs.snapshot_date
WHERE product_snapshots.snapshot_date >= '2025-01-01'
  AND product_snapshots.snapshot_date < '2025-07-01'
GROUP BY 1, 2, 3