-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_044
-- Generated: 2025-09-15T14:22:41Z

SELECT
  channel,
  COUNT(*) AS cnt,
  AVG(score) AS avg_val
FROM `project.dataset.users`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-02-01')
GROUP BY channel
HAVING avg_val > 0