-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_050
-- Generated: 2025-09-15T08:06:44Z

SELECT
  customer_id,
  DATEADD(day, 7, processed_at) AS next_week,
  ISNULL(quantity, 0) AS safe_metric
FROM `project.dataset.inventory`
WHERE processed_at >= '2025-05-01'