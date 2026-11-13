-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_032
-- Generated: 2025-09-15T14:42:00Z

-- Task: bq_032
-- This query users analysis

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