-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_022
-- Generated: 2025-09-15T17:45:00Z

-- Task: bq_022
-- This query clicks analysis

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