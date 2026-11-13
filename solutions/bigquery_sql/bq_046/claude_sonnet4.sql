-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_046
-- Generated: 2025-09-15T10:50:25Z

WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY product_id ORDER BY updated_at DESC
    ) AS _rn
  FROM `project.dataset.logs`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-09-01')
)
SELECT
  a.campaign_id,
  a.event_time,
  b.revenue
FROM deduped a
INNER JOIN `project.dataset.inventory` b
  ON a.product_id = b.product_id
WHERE a._rn = 1