-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_057
-- Generated: 2025-09-15T14:42:00Z

-- Task: bq_057
-- This query products analysis

WITH base AS (
  SELECT
    customer_id,
    ts,
    score
  FROM `project.dataset.products`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-06-01')
    AND customer_id IS NOT NULL
)
SELECT
  customer_id,
  COUNT(DISTINCT ts) AS unique_tss,
  SUM(score) AS total_score,
  AVG(score) AS avg_score
FROM base
GROUP BY customer_id
ORDER BY total_score DESC