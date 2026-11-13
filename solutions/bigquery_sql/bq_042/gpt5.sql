-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_042
-- Generated: 2025-09-15T14:18:00Z

-- Task: bq_042
-- This query subscriptions analysis

SELECT
  a.user_id,
  b.ts,
  SUM(a.revenue) AS total
FROM `project.dataset.subscriptions` a
JOIN `project.dataset.shipments` b
  ON a.user_id = b.user_id
WHERE a._PARTITIONTIME >= TIMESTAMP('2025-03-01')
GROUP BY 1, 2