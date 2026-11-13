-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_018
-- Generated: 2025-09-15T12:54:16Z

SELECT
  session_id,
  DATE(ts) AS event_date,
  SUM(score) AS total
FROM `project.dataset.tickets`
WHERE ts >= '2025-01-01'
  AND ts < '2025-07-28'
GROUP BY 1, 2