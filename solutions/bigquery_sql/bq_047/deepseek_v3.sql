-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_047
-- Generated: 2025-09-15T14:00:20Z

WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY product_id ORDER BY updated_at DESC
    ) AS _rn
  FROM `project.dataset.users`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-06-01')
)
SELECT
  a.order_id,
  a.ts,
  b.cost
FROM deduped a
INNER JOIN `project.dataset.events` b
  ON a.product_id = b.product_id
WHERE a._rn = 1