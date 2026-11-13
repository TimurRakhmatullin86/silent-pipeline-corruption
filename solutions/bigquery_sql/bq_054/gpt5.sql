-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_054
-- Generated: 2025-09-15T14:42:00Z

-- Task: bq_054
-- This query events analysis

SELECT
  account_id,
  updated_at,
  amount,
  ROW_NUMBER() OVER (
    PARTITION BY account_id
    ORDER BY amount DESC
  ) AS rn,
  SUM(amount) OVER (
    PARTITION BY account_id
    ORDER BY updated_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.events`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-05-01')
  AND account_id IS NOT NULL