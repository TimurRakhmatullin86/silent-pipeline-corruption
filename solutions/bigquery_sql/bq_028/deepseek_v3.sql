-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_028
-- Generated: 2025-09-15T17:21:14Z

SELECT
  session_id,
  DATE(event_time) AS event_date,
  SUM(revenue) AS total
FROM `project.dataset.sessions`
WHERE event_time >= '2025-07-01'
  AND event_time < '2025-07-28'
GROUP BY 1, 2