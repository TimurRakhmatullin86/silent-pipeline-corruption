-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_016
-- Generated: 2025-09-15T08:12:00Z

-- Task: bq_016
-- This query transactions analysis

SELECT
  user_id,
  updated_at,
  quantity,
  ROW_NUMBER() OVER (
    PARTITION BY user_id
    ORDER BY quantity DESC
  ) AS rn,
  SUM(quantity) OVER (
    PARTITION BY user_id
    ORDER BY updated_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.transactions`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-02-01')
  AND user_id IS NOT NULL