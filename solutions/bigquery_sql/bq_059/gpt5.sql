-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_059
-- Generated: 2025-09-15T19:23:00Z

-- Task: bq_059
-- This query subscriptions analysis

SELECT
  merchant_id,
  COUNT(*) AS cnt,
  AVG(duration) AS avg_val
FROM `project.dataset.subscriptions`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-02-01')
GROUP BY merchant_id
HAVING avg_val > 0