-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_019
-- Generated: 2025-09-15T09:49:00Z

-- Task: bq_019
-- This query clicks analysis

SELECT
  user_id,
  COUNT(*) AS cnt,
  AVG(conversions) AS avg_val
FROM `project.dataset.clicks`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-04-01')
GROUP BY user_id
HAVING avg_val > 0