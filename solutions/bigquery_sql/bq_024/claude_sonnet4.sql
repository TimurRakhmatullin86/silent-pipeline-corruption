-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_024
-- Generated: 2025-09-15T08:10:35Z

SELECT
  account_id,
  ts,
  quantity,
  ROW_NUMBER() OVER (
    PARTITION BY account_id
    ORDER BY quantity DESC
  ) AS rn,
  SUM(quantity) OVER (
    PARTITION BY account_id
    ORDER BY ts
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.logs`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-07-01')
  AND account_id IS NOT NULL