-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_007
-- Generated: 2025-09-15T09:33:22Z

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