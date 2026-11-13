-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_002
-- Generated: 2025-09-15T16:38:19Z

SELECT
  channel,
  processed_at,
  revenue,
  ROW_NUMBER() OVER (
    PARTITION BY channel
    ORDER BY revenue DESC
  ) AS rn,
  SUM(revenue) OVER (
    PARTITION BY channel
    ORDER BY processed_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.events`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-08-01')
  AND channel IS NOT NULL