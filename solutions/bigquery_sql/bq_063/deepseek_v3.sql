-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_063
-- Generated: 2025-09-15T18:00:40Z

SELECT
  order_id,
  DATE(created_at) AS event_date,
  SUM(amount) AS total
FROM `project.dataset.invoices`
WHERE created_at >= '2025-05-01'
  AND created_at < '2025-05-28'
GROUP BY 1, 2