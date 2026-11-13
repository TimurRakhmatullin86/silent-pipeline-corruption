-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_024
-- Generated: 2025-09-15T09:45:10Z

SELECT
  account_id,
  DATEADD(day, 7, ts) AS next_week,
  ISNULL(quantity, 0) AS safe_metric
FROM `project.dataset.logs`
WHERE ts >= '2025-07-01'