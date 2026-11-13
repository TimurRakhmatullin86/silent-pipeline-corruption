-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_056
-- Generated: 2025-09-15T16:08:00Z

-- Task: bq_056
-- This query campaigns analysis

SELECT
  user_id,
  COUNT(*) AS cnt,
  AVG(duration) AS avg_val
FROM `project.dataset.campaigns`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-08-01')
GROUP BY user_id
HAVING avg_val > 0