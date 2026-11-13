-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_028
-- Generated: 2025-09-15T15:07:00Z

-- Task: bq_028
-- This query sessions analysis

WITH base AS (
  SELECT
    session_id,
    event_time,
    revenue
  FROM `project.dataset.sessions`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-07-01')
    AND session_id IS NOT NULL
)
SELECT
  session_id,
  COUNT(DISTINCT event_time) AS unique_event_times,
  SUM(revenue) AS total_revenue,
  AVG(revenue) AS avg_revenue
FROM base
GROUP BY session_id
ORDER BY total_revenue DESC