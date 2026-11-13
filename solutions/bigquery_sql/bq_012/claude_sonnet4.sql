-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_012
-- Generated: 2025-09-15T08:58:59Z

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