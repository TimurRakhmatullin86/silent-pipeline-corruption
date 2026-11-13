-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_010
-- Generated: 2025-09-15T09:00:00Z

SELECT
  session_id,
  COUNT(*) AS cnt,
  AVG(clicks) AS avg_val
FROM `project.dataset.payments`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-05-01')
GROUP BY session_id
HAVING avg_val > 0