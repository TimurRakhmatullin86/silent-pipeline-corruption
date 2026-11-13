-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_058
-- Generated: 2025-09-15T09:24:12Z

WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY customer_id ORDER BY updated_at DESC
    ) AS _rn
  FROM `project.dataset.sessions`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-07-01')
)
SELECT
  a.session_id,
  a.updated_at,
  b.amount
FROM deduped a
INNER JOIN `project.dataset.events` b
  ON a.customer_id = b.customer_id
WHERE a._rn = 1