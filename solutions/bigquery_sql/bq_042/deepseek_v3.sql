-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_042
-- Generated: 2025-09-15T16:54:36Z

WITH base AS (
  SELECT
    user_id,
    ts,
    revenue
  FROM `project.dataset.subscriptions`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-03-01')
    AND user_id IS NOT NULL
)
SELECT
  user_id,
  COUNT(DISTINCT ts) AS unique_tss,
  SUM(revenue) AS total_revenue,
  AVG(revenue) AS avg_revenue
FROM base
GROUP BY user_id
ORDER BY total_revenue DESC