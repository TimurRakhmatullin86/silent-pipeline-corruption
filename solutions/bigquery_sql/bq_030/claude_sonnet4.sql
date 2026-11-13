-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_030
-- Generated: 2025-09-15T17:04:32Z

SELECT
  a.account_id,
  b.processed_at,
  SUM(a.cost) AS total
FROM `project.dataset.products` a
JOIN `project.dataset.invoices` b
  ON a.account_id = b.account_id
WHERE a._PARTITIONTIME >= TIMESTAMP('2025-02-01')
GROUP BY 1, 2