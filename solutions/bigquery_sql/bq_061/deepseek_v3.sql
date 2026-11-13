-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_061
-- Generated: 2025-09-15T13:09:06Z

WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY order_id ORDER BY updated_at DESC
    ) AS _rn
  FROM `project.dataset.transactions`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-06-01')
)
SELECT
  a.session_id,
  a.event_time,
  b.duration
FROM deduped a
INNER JOIN `project.dataset.products` b
  ON a.order_id = b.order_id
WHERE a._rn = 1