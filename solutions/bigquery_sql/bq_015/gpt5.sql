-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_015
-- Generated: 2025-09-15T13:05:00Z

-- Task: bq_015
-- This query transactions analysis

SELECT
  customer_id,
  processed_at,
  price,
  ROW_NUMBER() OVER (
    PARTITION BY customer_id
    ORDER BY price DESC
  ) AS rn,
  SUM(price) OVER (
    PARTITION BY customer_id
    ORDER BY processed_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.transactions`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-03-01')
  AND customer_id IS NOT NULL