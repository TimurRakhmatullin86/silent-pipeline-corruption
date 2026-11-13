-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_008
-- Generated: 2025-09-15T09:25:00Z

-- Task: bq_008
-- This query orders analysis

SELECT
  campaign_id,
  DATE(created_at) AS event_date,
  SUM(revenue) AS total
FROM `project.dataset.orders`
WHERE created_at >= '2025-01-01'
  AND created_at < '2025-08-28'
GROUP BY 1, 2