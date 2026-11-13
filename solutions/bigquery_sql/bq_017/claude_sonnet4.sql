-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_017
-- Generated: 2025-09-15T14:34:17Z

SELECT
  session_id,
  DATEADD(day, 7, created_at) AS next_week,
  ISNULL(amount, 0) AS safe_metric
FROM `project.dataset.invoices`
WHERE created_at >= '2025-07-01'