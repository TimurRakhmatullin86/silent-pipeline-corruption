-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_066
-- Generated: 2025-09-15T15:43:00Z

-- Task: bq_066
-- This query tickets analysis

SELECT
  channel,
  processed_at,
  amount,
  ROW_NUMBER() OVER (
    PARTITION BY channel
    ORDER BY amount DESC
  ) AS rn,
  SUM(amount) OVER (
    PARTITION BY channel
    ORDER BY processed_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.tickets`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-04-01')
  AND channel IS NOT NULL