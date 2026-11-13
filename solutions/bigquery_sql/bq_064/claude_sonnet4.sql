-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_064
-- Generated: 2025-09-15T14:10:05Z

WITH base AS (
  SELECT
    session_id,
    created_at,
    revenue
  FROM `project.dataset.subscriptions`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-08-01')
    AND session_id IS NOT NULL
)
SELECT
  session_id,
  COUNT(DISTINCT created_at) AS unique_created_ats,
  SUM(revenue) AS total_revenue,
  AVG(revenue) AS avg_revenue
FROM base
GROUP BY session_id
ORDER BY total_revenue DESC