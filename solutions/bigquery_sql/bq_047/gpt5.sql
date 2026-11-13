-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_047
-- Generated: 2025-09-15T12:40:00Z

-- Task: bq_047
-- This query users analysis

WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY product_id ORDER BY updated_at DESC
    ) AS _rn
  FROM `project.dataset.users`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-06-01')
)
SELECT
  a.order_id,
  a.ts,
  b.cost
FROM deduped a
INNER JOIN `project.dataset.events` b
  ON a.product_id = b.product_id
WHERE a._rn = 1