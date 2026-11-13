-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_051
-- Generated: 2025-09-15T18:06:33Z

SELECT
  customer_id,
  created_at,
  duration,
  ROW_NUMBER() OVER (
    PARTITION BY customer_id
    ORDER BY duration DESC
  ) AS rn,
  SUM(duration) OVER (
    PARTITION BY customer_id
    ORDER BY created_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.clicks`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-05-01')
  AND customer_id IS NOT NULL