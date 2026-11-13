-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_040
-- Generated: 2025-09-15T18:58:00Z

-- Task: bq_040
-- This query orders analysis

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