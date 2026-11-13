-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_065
-- Generated: 2025-09-15T11:27:00Z

-- Task: bq_065
-- This query sessions analysis

SELECT
  channel,
  COUNT(*) AS cnt,
  AVG(clicks) AS avg_val
FROM `project.dataset.sessions`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-06-01')
GROUP BY channel
HAVING avg_val > 0