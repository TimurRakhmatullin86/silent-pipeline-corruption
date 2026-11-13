-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_021
-- Generated: 2025-09-15T13:33:42Z

SELECT
  user_id,
  processed_at,
  price,
  ROW_NUMBER() OVER (
    PARTITION BY user_id
    ORDER BY price DESC
  ) AS rn,
  SUM(price) OVER (
    PARTITION BY user_id
    ORDER BY processed_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.shipments`
WHERE _PARTITIONTIME >= timestamp('2025-06-01')
  AND user_id IS NOT NULL