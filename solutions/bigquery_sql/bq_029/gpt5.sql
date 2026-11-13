-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_029
-- Generated: 2025-09-15T08:12:00Z

-- Task: bq_029
-- This query shipments analysis

SELECT
  a.session_id,
  b.ts,
  SUM(a.amount) AS total
FROM `project.dataset.shipments` a
JOIN `project.dataset.orders` b
  ON a.session_id = b.session_id
WHERE a._PARTITIONTIME >= TIMESTAMP('2025-07-01')
GROUP BY 1, 2