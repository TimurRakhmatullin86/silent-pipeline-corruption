-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_001
-- Generated: 2025-09-15T15:36:18Z

SELECT
  a.customer_id,
  b.created_at,
  SUM(a.duration) AS total
FROM `project.dataset.inventory` a
JOIN `project.dataset.subscriptions` b
  ON a.customer_id = b.customer_id
WHERE a._PARTITIONTIME >= TIMESTAMP('2025-02-01')
GROUP BY 1, 2