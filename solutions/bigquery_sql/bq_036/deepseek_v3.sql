-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_036
-- Generated: 2025-09-15T17:45:50Z

SELECT
  user_id,
  updated_at,
  clicks,
  ROW_NUMBER() OVER (
    PARTITION BY user_id
    ORDER BY clicks DESC
  ) AS rn,
  SUM(clicks) OVER (
    PARTITION BY user_id
    ORDER BY updated_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.transactions`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-02-01')
  AND user_id IS NOT NULL