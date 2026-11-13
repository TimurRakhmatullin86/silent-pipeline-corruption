-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_066
-- Generated: 2025-09-15T16:26:43Z

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