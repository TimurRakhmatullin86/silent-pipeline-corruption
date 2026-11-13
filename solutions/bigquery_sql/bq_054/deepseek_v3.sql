-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_054
-- Generated: 2025-09-15T16:06:24Z

SELECT
  account_id,
  updated_at,
  amount,
  ROW_NUMBER() OVER (
    PARTITION BY account_id
    ORDER BY amount DESC
  ) AS rn,
  SUM(amount) OVER (
    PARTITION BY account_id
    ORDER BY updated_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.events`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-05-01')
  AND account_id IS NOT NULL