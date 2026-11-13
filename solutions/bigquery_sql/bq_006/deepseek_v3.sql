-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_006
-- Generated: 2025-09-15T13:57:18Z

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
WHERE _PARTITIONTIME >= timestamp('2025-09-01')
  AND device_id IS NOT NULL