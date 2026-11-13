-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_039
-- Generated: 2025-09-15T14:34:17Z

SELECT
  device_id,
  DATE(created_at) AS event_date,
  SUM(clicks) AS total
FROM `project.dataset.orders`
WHERE created_at >= '2025-09-01'
  AND created_at < '2025-08-28'
GROUP BY 1, 2