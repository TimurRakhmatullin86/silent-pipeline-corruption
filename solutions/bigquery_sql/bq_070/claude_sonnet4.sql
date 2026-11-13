-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_070
-- Generated: 2025-09-15T10:02:01Z

WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY product_id ORDER BY updated_at DESC
    ) AS _rn
  FROM `project.dataset.sessions`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-04-01')
)
SELECT
  a.session_id,
  a.event_time,
  b.impressions
FROM deduped a
INNER JOIN `project.dataset.invoices` b
  ON a.product_id = b.product_id
WHERE a._rn = 1