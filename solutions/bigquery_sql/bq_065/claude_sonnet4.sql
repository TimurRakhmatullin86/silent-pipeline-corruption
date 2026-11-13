-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_065
-- Generated: 2025-09-15T12:54:27Z

SELECT
  channel,
  COUNT(*) AS cnt,
  AVG(clicks) AS avg_val
FROM `project.dataset.sessions`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-06-01')
GROUP BY channel
HAVING avg_val > 0