-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_027
-- Generated: 2025-09-15T15:51:34Z

WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY order_id ORDER BY updated_at DESC
    ) AS _rn
  FROM `project.dataset.shipments`
  WHERE _PARTITIONTIME >= timestamp('2025-01-01')
)
SELECT
  a.account_id,
  a.updated_at,
  b.score
FROM deduped a
INNER JOIN `project.dataset.orders` b
  ON a.order_id = b.order_id
WHERE a._rn = 1