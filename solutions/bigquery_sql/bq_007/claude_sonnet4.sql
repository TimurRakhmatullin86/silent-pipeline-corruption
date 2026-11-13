-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_007
-- Generated: 2025-09-15T08:22:11Z

SELECT
  channel,
  updated_at,
  quantity,
  ROW_NUMBER() OVER (
    PARTITION BY channel
    ORDER BY quantity DESC
  ) AS rn,
  SUM(quantity) OVER (
    PARTITION BY channel
    ORDER BY updated_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.transactions`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-09-01')
  AND channel IS NOT NULL