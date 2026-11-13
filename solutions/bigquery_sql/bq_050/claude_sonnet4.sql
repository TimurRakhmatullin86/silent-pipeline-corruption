-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_050
-- Generated: 2025-09-15T19:44:22Z

SELECT
  customer_id,
  DATE(processed_at) AS event_date,
  SUM(quantity) AS total
FROM `project.dataset.inventory`
WHERE processed_at >= '2025-05-01'
  AND processed_at < '2025-01-28'
GROUP BY 1, 2