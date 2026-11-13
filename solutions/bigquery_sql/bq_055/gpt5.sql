-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_055
-- Generated: 2025-09-15T11:39:00Z

-- Task: bq_055
-- This query products analysis

WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY order_id ORDER BY updated_at DESC
    ) AS _rn
  FROM `project.dataset.products`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-01-01')
)
SELECT
  a.session_id,
  a.ts,
  b.amount
FROM deduped a
INNER JOIN `project.dataset.campaigns` b
  ON a.order_id = b.order_id
WHERE a._rn = 1