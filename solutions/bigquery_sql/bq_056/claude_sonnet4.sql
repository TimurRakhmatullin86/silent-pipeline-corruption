-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_056
-- Generated: 2025-09-15T17:16:08Z

SELECT
  a.user_id,
  b.updated_at,
  SUM(a.duration) AS total
FROM `project.dataset.campaigns` a
JOIN `project.dataset.payments` b
  ON a.user_id = b.user_id
WHERE a._PARTITIONTIME >= TIMESTAMP('2025-08-01')
GROUP BY 1, 2