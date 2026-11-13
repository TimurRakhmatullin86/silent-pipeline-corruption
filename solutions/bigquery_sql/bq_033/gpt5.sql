-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_033
-- Generated: 2025-09-15T08:24:00Z

-- Task: bq_033
-- This query inventory analysis

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