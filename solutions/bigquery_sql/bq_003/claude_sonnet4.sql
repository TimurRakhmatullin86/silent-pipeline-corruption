-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_003
-- Generated: 2025-09-15T10:02:01Z

WITH base AS (
  SELECT
    user_id,
    event_time,
    price
  FROM `project.dataset.clicks`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-03-01')
    AND user_id IS NOT NULL
)
SELECT
  user_id,
  COUNT(DISTINCT event_time) AS unique_event_times,
  SUM(price) AS total_price,
  AVG(price) AS avg_price
FROM base
GROUP BY user_id
ORDER BY total_price DESC