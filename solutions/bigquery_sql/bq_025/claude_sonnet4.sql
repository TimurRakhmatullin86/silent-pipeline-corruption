-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_025
-- Generated: 2025-09-15T10:14:37Z

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