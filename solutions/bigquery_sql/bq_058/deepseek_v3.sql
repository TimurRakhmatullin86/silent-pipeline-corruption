-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_058
-- Generated: 2025-09-15T10:36:24Z

SELECT
  session_id,
  DATE(updated_at) AS event_date,
  SUM(amount) AS total
FROM `project.dataset.sessions`
WHERE updated_at >= '2025-07-01'
  AND updated_at < '2025-08-28'
GROUP BY 1, 2