-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_058
-- Generated: 2025-09-15T08:12:00Z

-- Task: bq_058
-- This query sessions analysis

SELECT
  session_id,
  COUNT(*) AS cnt,
  AVG(amount) AS avg_val
FROM `project.dataset.sessions`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-07-01')
GROUP BY session_id
HAVING avg_val > 0