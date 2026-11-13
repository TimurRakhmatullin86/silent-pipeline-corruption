-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_052
-- Generated: 2025-09-15T15:24:42Z

WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY product_id ORDER BY updated_at DESC
    ) AS _rn
  FROM `project.dataset.transactions`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-09-01')
)
SELECT
  a.product_id,
  a.created_at,
  b.price
FROM deduped a
INNER JOIN `project.dataset.shipments` b
  ON a.product_id = b.product_id
WHERE a._rn = 1