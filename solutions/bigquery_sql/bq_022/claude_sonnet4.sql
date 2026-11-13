-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_022
-- Generated: 2025-09-15T18:30:45Z

WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY order_id ORDER BY updated_at DESC
    ) AS _rn
  FROM `project.dataset.clicks`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-06-01')
)
SELECT
  a.channel,
  a.event_time,
  b.clicks
FROM deduped a
INNER JOIN `project.dataset.inventory` b
  ON a.order_id = b.order_id
WHERE a._rn = 1