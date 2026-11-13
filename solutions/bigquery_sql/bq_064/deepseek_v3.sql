-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_064
-- Generated: 2025-09-15T15:15:10Z

SELECT
  session_id,
  DATE(created_at) AS event_date,
  SUM(revenue) AS total
FROM `project.dataset.subscriptions`
WHERE created_at >= '2025-08-01'
  AND created_at < '2025-01-28'
GROUP BY 1, 2