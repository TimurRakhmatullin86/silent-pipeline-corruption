-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_021
-- Generated: 2025-09-15T11:51:00Z

-- Task: bq_021
-- This query shipments analysis

SELECT
  user_id,
  COUNT(*) AS cnt,
  AVG(price) AS avg_val
FROM `project.dataset.shipments`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-06-01')
GROUP BY user_id
HAVING avg_val > 0