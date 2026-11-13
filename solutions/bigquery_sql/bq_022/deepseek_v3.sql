-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_022
-- Generated: 2025-09-15T19:15:30Z

SELECT
  channel,
  DATEADD(day, 7, event_time) AS next_week,
  ISNULL(clicks, 0) AS safe_metric
FROM `project.dataset.clicks`
WHERE event_time >= '2025-06-01'