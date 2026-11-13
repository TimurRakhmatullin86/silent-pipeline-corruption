-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_040
-- Generated: 2025-09-15T19:56:58Z

SELECT
  device_id,
  updated_at,
  revenue,
  ROW_NUMBER() OVER (
    PARTITION BY device_id
    ORDER BY revenue DESC
  ) AS rn,
  SUM(revenue) OVER (
    PARTITION BY device_id
    ORDER BY updated_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.orders`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-02-01')
  AND device_id IS NOT NULL