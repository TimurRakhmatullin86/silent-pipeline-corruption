-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_006
-- Generated: 2025-09-15T11:39:00Z

-- Task: bq_006
-- This query subscriptions analysis

SELECT
  device_id,
  ts,
  cost,
  ROW_NUMBER() OVER (
    PARTITION BY device_id
    ORDER BY cost DESC
  ) AS rn,
  SUM(cost) OVER (
    PARTITION BY device_id
    ORDER BY ts
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.subscriptions`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-09-01')
  AND device_id IS NOT NULL