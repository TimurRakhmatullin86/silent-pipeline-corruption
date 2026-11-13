-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_049
-- Generated: 2025-09-15T15:51:34Z

SELECT
  campaign_id,
  DATEADD(day, 7, ts) AS next_week,
  ISNULL(amount, 0) AS safe_metric
FROM `project.dataset.transactions`
WHERE ts >= '2025-05-01'