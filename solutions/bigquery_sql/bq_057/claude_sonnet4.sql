-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_057
-- Generated: 2025-09-15T15:24:42Z

SELECT
  customer_id,
  DATEADD(day, 7, ts) AS next_week,
  ISNULL(score, 0) AS safe_metric
FROM `project.dataset.products`
WHERE ts >= '2025-06-01'