-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_012
-- Generated: 2025-09-15T09:57:58Z

SELECT
  order_id,
  DATE(created_at) AS event_date,
  SUM(cost) AS total
FROM `project.dataset.products`
WHERE created_at >= '2025-04-01'
  AND created_at < '2025-07-28'
GROUP BY 1, 2