-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_023
-- Generated: 2025-09-15T12:42:28Z

SELECT
  account_id,
  DATE(ts) AS event_date,
  SUM(cost) AS total
FROM `project.dataset.products`
WHERE ts >= '2025-03-01'
  AND ts < '2025-09-28'
GROUP BY 1, 2