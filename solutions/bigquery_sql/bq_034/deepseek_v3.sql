-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_034
-- Generated: 2025-09-15T18:00:40Z

SELECT
  session_id,
  DATE(event_time) AS event_date,
  SUM(impressions) AS total
FROM `project.dataset.payments`
WHERE event_time >= '2025-02-01'
  AND event_time < '2025-06-28'
GROUP BY 1, 2