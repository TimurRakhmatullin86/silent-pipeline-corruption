-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_051
-- Generated: 2025-09-15T19:39:06Z

SELECT
  customer_id,
  DATEADD(day, 7, created_at) AS next_week,
  ISNULL(duration, 0) AS safe_metric
FROM `project.dataset.clicks`
WHERE created_at >= '2025-05-01'