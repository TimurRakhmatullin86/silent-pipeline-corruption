-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_066
-- Generated: 2025-09-15T17:09:26Z

SELECT
  channel,
  DATE(processed_at) AS event_date,
  SUM(amount) AS total
FROM `project.dataset.tickets`
WHERE processed_at >= '2025-04-01'
  AND processed_at < '2025-03-28'
GROUP BY 1, 2