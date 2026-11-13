-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_011
-- Generated: 2025-09-15T08:18:32Z

SELECT
  session_id,
  created_at,
  clicks,
  ROW_NUMBER() OVER (
    PARTITION BY session_id
    ORDER BY clicks DESC
  ) AS rn,
  SUM(clicks) OVER (
    PARTITION BY session_id
    ORDER BY created_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.products`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-06-01')
  AND session_id IS NOT NULL