-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_043
-- Generated: 2025-09-15T15:24:42Z

WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY session_id ORDER BY updated_at DESC
    ) AS _rn
  FROM `project.dataset.payments`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-07-01')
)
SELECT
  a.merchant_id,
  a.ts,
  b.duration
FROM deduped a
INNER JOIN `project.dataset.inventory` b
  ON a.session_id = b.session_id
WHERE a._rn = 1