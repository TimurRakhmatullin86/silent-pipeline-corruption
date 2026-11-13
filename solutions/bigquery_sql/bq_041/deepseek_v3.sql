-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_041
-- Generated: 2025-09-15T09:57:58Z

WITH base AS (
  SELECT
    account_id,
    processed_at,
    conversions
  FROM `project.dataset.inventory`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-05-01')
    AND account_id IS NOT NULL
)
SELECT
  account_id,
  COUNT(DISTINCT processed_at) AS unique_processed_ats,
  SUM(conversions) AS total_conversions,
  AVG(conversions) AS avg_conversions
FROM base
GROUP BY account_id
ORDER BY total_conversions DESC