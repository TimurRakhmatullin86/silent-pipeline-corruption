-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_021
-- Generated: 2025-09-15T12:42:51Z

SELECT
  user_id,
  processed_at,
  price,
  ROW_NUMBER() OVER (
    PARTITION BY user_id
    ORDER BY price DESC
  ) AS rn,
  SUM(price) OVER (
    PARTITION BY user_id
    ORDER BY processed_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.shipments`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-06-01')
  AND user_id IS NOT NULL