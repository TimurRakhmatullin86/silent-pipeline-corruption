-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_019
-- Generated: 2025-09-15T11:27:38Z

SELECT
  user_id,
  ts,
  conversions,
  ROW_NUMBER() OVER (
    PARTITION BY user_id
    ORDER BY conversions DESC
  ) AS rn,
  SUM(conversions) OVER (
    PARTITION BY user_id
    ORDER BY ts
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.clicks`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-04-01')
  AND user_id IS NOT NULL