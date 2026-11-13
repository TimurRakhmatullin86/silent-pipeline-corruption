-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_010
-- Generated: 2025-09-15T10:00:00Z

SELECT
  session_id,
  DATEADD(day, 7, ts) AS next_week,
  ISNULL(clicks, 0) AS safe_metric
FROM `project.dataset.payments`
WHERE ts >= '2025-05-01'