-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_034
-- Generated: 2025-09-15T17:40:20Z

WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY order_id ORDER BY updated_at DESC
    ) AS _rn
  FROM `project.dataset.payments`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-02-01')
)
SELECT
  a.session_id,
  a.event_time,
  b.impressions
FROM deduped a
INNER JOIN `project.dataset.subscriptions` b
  ON a.order_id = b.order_id
WHERE a._rn = 1