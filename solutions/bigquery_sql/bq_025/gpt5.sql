-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_025
-- Generated: 2025-09-15T09:37:00Z

-- Task: bq_025
-- This query payments analysis

WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY product_id ORDER BY updated_at DESC
    ) AS _rn
  FROM `project.dataset.payments`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-06-01')
)
SELECT
  a.user_id,
  a.ts,
  b.revenue
FROM deduped a
INNER JOIN `project.dataset.orders` b
  ON a.product_id = b.product_id
WHERE a._rn = 1