-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_012
-- Generated: 2025-09-15T19:59:00Z

-- Task: bq_012
-- This query products analysis

WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY order_id ORDER BY updated_at DESC
    ) AS _rn
  FROM `project.dataset.products`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-04-01')
)
SELECT
  a.order_id,
  a.created_at,
  b.cost
FROM deduped a
INNER JOIN `project.dataset.transactions` b
  ON a.order_id = b.order_id
WHERE a._rn = 1