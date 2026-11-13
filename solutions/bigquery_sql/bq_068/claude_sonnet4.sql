-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_068
-- Generated: 2025-09-15T10:26:13Z

SELECT
  merchant_id,
  DATEADD(day, 7, updated_at) AS next_week,
  ISNULL(cost, 0) AS safe_metric
FROM `project.dataset.orders`
WHERE updated_at >= '2025-09-01'