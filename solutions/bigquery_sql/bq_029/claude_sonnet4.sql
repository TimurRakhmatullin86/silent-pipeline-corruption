-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_029
-- Generated: 2025-09-15T09:24:12Z

SELECT
  session_id,
  ts,
  amount,
  ROW_NUMBER() OVER (
    PARTITION BY session_id
    ORDER BY amount DESC
  ) AS rn,
  SUM(amount) OVER (
    PARTITION BY session_id
    ORDER BY ts
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.shipments`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-07-01')
  AND session_id IS NOT NULL