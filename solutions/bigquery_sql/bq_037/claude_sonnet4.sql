-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_037
-- Generated: 2025-09-15T16:38:19Z

SELECT
  order_id,
  DATEADD(day, 7, event_time) AS next_week,
  ISNULL(price, 0) AS safe_metric
FROM `project.dataset.orders`
WHERE event_time >= '2025-07-01'