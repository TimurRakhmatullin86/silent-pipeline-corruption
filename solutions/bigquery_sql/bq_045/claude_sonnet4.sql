-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_045
-- Generated: 2025-09-15T08:10:35Z

WITH base AS (
  SELECT
    customer_id,
    event_time,
    clicks
  FROM `project.dataset.sessions`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-01-01')
    AND customer_id IS NOT NULL
)
SELECT
  customer_id,
  COUNT(DISTINCT event_time) AS unique_event_times,
  SUM(clicks) AS total_clicks,
  AVG(clicks) AS avg_clicks
FROM base
GROUP BY customer_id
ORDER BY total_clicks DESC