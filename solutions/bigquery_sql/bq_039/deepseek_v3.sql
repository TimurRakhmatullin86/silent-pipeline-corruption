-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_039
-- Generated: 2025-09-15T15:51:34Z

WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY customer_id ORDER BY updated_at DESC
    ) AS _rn
  FROM `project.dataset.orders`
  WHERE _PARTITIONTIME >= timestamp('2025-09-01')
)
SELECT
  a.device_id,
  a.created_at,
  b.clicks
FROM deduped a
INNER JOIN `project.dataset.clicks` b
  ON a.customer_id = b.customer_id
WHERE a._rn = 1