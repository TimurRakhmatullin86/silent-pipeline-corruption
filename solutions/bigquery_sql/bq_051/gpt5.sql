-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_051
-- Generated: 2025-09-15T17:33:00Z

-- Task: bq_051
-- This query clicks analysis

SELECT
  customer_id,
  DATE(created_at) AS event_date,
  SUM(duration) AS total
FROM `project.dataset.clicks`
WHERE created_at >= '2025-05-01'
  AND created_at < '2025-05-28'
GROUP BY 1, 2