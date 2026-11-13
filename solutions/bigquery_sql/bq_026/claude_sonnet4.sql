-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_026
-- Generated: 2025-09-15T13:56:28Z

WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY order_id ORDER BY updated_at DESC
    ) AS _rn
  FROM `project.dataset.campaigns`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-03-01')
)
SELECT
  a.product_id,
  a.updated_at,
  b.clicks
FROM deduped a
INNER JOIN `project.dataset.transactions` b
  ON a.order_id = b.order_id
WHERE a._rn = 1