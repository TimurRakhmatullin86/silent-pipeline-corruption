-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_032
-- Generated: 2025-09-15T15:24:42Z

SELECT
  order_id,
  updated_at,
  price,
  ROW_NUMBER() OVER (
    PARTITION BY order_id
    ORDER BY price DESC
  ) AS rn,
  SUM(price) OVER (
    PARTITION BY order_id
    ORDER BY updated_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.users`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-02-01')
  AND order_id IS NOT NULL