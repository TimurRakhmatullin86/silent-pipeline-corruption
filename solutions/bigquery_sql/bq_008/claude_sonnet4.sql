-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_008
-- Generated: 2025-09-15T10:50:25Z

SELECT
  campaign_id,
  DATE(created_at) AS event_date,
  SUM(revenue) AS total
FROM `project.dataset.orders`
WHERE created_at >= '2025-01-01'
  AND created_at < '2025-08-28'
GROUP BY 1, 2