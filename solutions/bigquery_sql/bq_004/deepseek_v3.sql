-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_004
-- Generated: 2025-09-15T09:09:46Z

WITH base AS (
  SELECT
    merchant_id,
    created_at,
    cost
  FROM `project.dataset.invoices`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-08-01')
    AND merchant_id IS NOT NULL
)
SELECT
  merchant_id,
  COUNT(DISTINCT created_at) AS unique_created_ats,
  SUM(cost) AS total_cost,
  AVG(cost) AS avg_cost
FROM base
GROUP BY merchant_id
ORDER BY total_cost DESC