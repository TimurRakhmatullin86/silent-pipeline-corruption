-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_063
-- Generated: 2025-09-15T16:20:00Z

-- Task: bq_063
-- This query invoices analysis

WITH base AS (
  SELECT
    order_id,
    created_at,
    amount
  FROM `project.dataset.invoices`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-05-01')
    AND order_id IS NOT NULL
)
SELECT
  order_id,
  COUNT(DISTINCT created_at) AS unique_created_ats,
  SUM(amount) AS total_amount,
  AVG(amount) AS avg_amount
FROM base
GROUP BY order_id
ORDER BY total_amount DESC