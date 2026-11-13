-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_024
-- Generated: 2025-09-15T19:35:00Z

-- Task: bq_024
-- This query logs analysis

SELECT
  account_id,
  COUNT(*) AS cnt,
  AVG(quantity) AS avg_val
FROM `project.dataset.logs`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-07-01')
GROUP BY account_id
HAVING avg_val > 0