-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_069
-- Generated: 2025-09-15T15:07:00Z

-- Task: bq_069
-- This query payments analysis

WITH base AS (
  SELECT
    session_id,
    updated_at,
    quantity
  FROM `project.dataset.payments`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-01-01')
    AND session_id IS NOT NULL
)
SELECT
  session_id,
  COUNT(DISTINCT updated_at) AS unique_updated_ats,
  SUM(quantity) AS total_quantity,
  AVG(quantity) AS avg_quantity
FROM base
GROUP BY session_id
ORDER BY total_quantity DESC