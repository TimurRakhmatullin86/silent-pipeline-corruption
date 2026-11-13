-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_018
-- Generated: 2025-09-15T11:16:38Z

SELECT
  session_id,
  COUNT(*) AS cnt,
  AVG(score) AS avg_val
FROM `project.dataset.tickets`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-01-01')
GROUP BY session_id
HAVING avg_val > 0