-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_027
-- Generated: 2025-09-15T14:34:17Z

SELECT
  account_id,
  DATE(updated_at) AS event_date,
  SUM(score) AS total
FROM `project.dataset.shipments`
WHERE updated_at >= '2025-01-01'
  AND updated_at < '2025-07-28'
GROUP BY 1, 2