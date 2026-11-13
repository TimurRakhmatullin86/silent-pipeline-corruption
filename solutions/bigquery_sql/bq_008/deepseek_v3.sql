-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_008
-- Generated: 2025-09-15T11:15:50Z

WITH base AS (
  SELECT
    campaign_id,
    created_at,
    revenue
  FROM `project.dataset.orders`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-01-01')
    AND campaign_id IS NOT NULL
)
SELECT
  campaign_id,
  COUNT(DISTINCT created_at) AS unique_created_ats,
  SUM(revenue) AS total_revenue,
  AVG(revenue) AS avg_revenue
FROM base
GROUP BY campaign_id
ORDER BY total_revenue DESC