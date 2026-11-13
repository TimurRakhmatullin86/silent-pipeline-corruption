-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_067
-- Generated: 2025-09-15T15:27:58Z

SELECT
  campaign_id,
  DATE(ts) AS event_date,
  SUM(duration) AS total
FROM `project.dataset.clicks`
WHERE ts >= '2025-02-01'
  AND ts < '2025-05-28'
GROUP BY 1, 2