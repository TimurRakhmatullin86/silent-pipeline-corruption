-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_068
-- Generated: 2025-09-15T09:13:00Z

-- Task: bq_068
-- This query orders analysis

WITH base AS (
  SELECT
    merchant_id,
    updated_at,
    cost
  FROM `project.dataset.orders`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-09-01')
    AND merchant_id IS NOT NULL
)
SELECT
  merchant_id,
  COUNT(DISTINCT updated_at) AS unique_updated_ats,
  SUM(cost) AS total_cost,
  AVG(cost) AS avg_cost
FROM base
GROUP BY merchant_id
ORDER BY total_cost DESC