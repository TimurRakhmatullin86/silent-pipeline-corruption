-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_059
-- Generated: 2025-09-15T08:46:23Z

WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY product_id ORDER BY updated_at DESC
    ) AS _rn
  FROM `project.dataset.subscriptions`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-02-01')
)
SELECT
  a.merchant_id,
  a.processed_at,
  b.duration
FROM deduped a
INNER JOIN `project.dataset.orders` b
  ON a.product_id = b.product_id
WHERE a._rn = 1