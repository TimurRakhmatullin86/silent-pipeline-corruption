-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_035
-- Generated: 2025-09-15T11:27:00Z

-- Task: bq_035
-- This query orders analysis

WITH base AS (
  SELECT
    account_id,
    updated_at,
    conversions
  FROM `project.dataset.orders`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-05-01')
    AND account_id IS NOT NULL
)
SELECT
  account_id,
  COUNT(DISTINCT updated_at) AS unique_updated_ats,
  SUM(conversions) AS total_conversions,
  AVG(conversions) AS avg_conversions
FROM base
GROUP BY account_id
ORDER BY total_conversions DESC