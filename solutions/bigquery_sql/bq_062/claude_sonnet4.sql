-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_062
-- Generated: 2025-09-15T19:32:46Z

WITH base AS (
  SELECT
    order_id,
    updated_at,
    duration
  FROM `project.dataset.transactions`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-06-01')
    AND order_id IS NOT NULL
)
SELECT
  order_id,
  COUNT(DISTINCT updated_at) AS unique_updated_ats,
  SUM(duration) AS total_duration,
  AVG(duration) AS avg_duration
FROM base
GROUP BY order_id
ORDER BY total_duration DESC