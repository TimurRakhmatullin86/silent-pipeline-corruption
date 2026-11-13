-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_060
-- Generated: 2025-09-15T12:06:04Z

WITH base AS (
  SELECT
    customer_id,
    ts,
    conversions
  FROM `project.dataset.users`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-05-01')
    AND customer_id IS NOT NULL
)
SELECT
  customer_id,
  COUNT(DISTINCT ts) AS unique_tss,
  SUM(conversions) AS total_conversions,
  AVG(conversions) AS avg_conversions
FROM base
GROUP BY customer_id
ORDER BY total_conversions DESC