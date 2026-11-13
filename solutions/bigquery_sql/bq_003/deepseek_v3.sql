-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_003
-- Generated: 2025-09-15T11:03:02Z

SELECT
  user_id,
  DATEADD(day, 7, event_time) AS next_week,
  ISNULL(price, 0) AS safe_metric
FROM `project.dataset.clicks`
WHERE event_time >= '2025-03-01'