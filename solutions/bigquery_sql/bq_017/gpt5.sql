-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_017
-- Generated: 2025-09-15T13:17:00Z

-- Task: bq_017
-- This query invoices analysis

SELECT
  session_id,
  created_at,
  amount,
  ROW_NUMBER() OVER (
    PARTITION BY session_id
    ORDER BY amount DESC
  ) AS rn,
  SUM(amount) OVER (
    PARTITION BY session_id
    ORDER BY created_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.invoices`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-07-01')
  AND session_id IS NOT NULL