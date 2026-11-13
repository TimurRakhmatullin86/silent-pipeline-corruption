-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_027
-- Generated: 2025-09-15T13:17:00Z

-- Task: bq_027
-- This query shipments analysis

WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY order_id ORDER BY updated_at DESC
    ) AS _rn
  FROM `project.dataset.shipments`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-01-01')
)
SELECT
  a.account_id,
  a.updated_at,
  b.score
FROM deduped a
INNER JOIN `project.dataset.orders` b
  ON a.order_id = b.order_id
WHERE a._rn = 1