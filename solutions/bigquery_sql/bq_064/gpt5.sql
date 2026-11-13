-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_064
-- Generated: 2025-09-15T13:05:00Z

-- Task: bq_064
-- This query subscriptions analysis

SELECT
  session_id,
  DATEADD(day, 7, created_at) AS next_week,
  ISNULL(revenue, 0) AS safe_metric
FROM `project.dataset.subscriptions`
WHERE created_at >= '2025-08-01'