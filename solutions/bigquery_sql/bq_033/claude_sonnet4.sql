-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_033
-- Generated: 2025-09-15T09:48:24Z

SELECT
  customer_id,
  updated_at,
  amount,
  ROW_NUMBER() OVER (
    PARTITION BY customer_id
    ORDER BY amount DESC
  ) AS rn,
  SUM(amount) OVER (
    PARTITION BY customer_id
    ORDER BY updated_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.inventory`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-07-01')
  AND customer_id IS NOT NULL