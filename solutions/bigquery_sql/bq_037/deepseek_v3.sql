-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_037
-- Generated: 2025-09-15T17:57:38Z

SELECT
  order_id,
  DATE(event_time) AS event_date,
  SUM(price) AS total
FROM `project.dataset.orders`
WHERE event_time >= '2025-07-01'
  AND event_time < '2025-03-28'
GROUP BY 1, 2