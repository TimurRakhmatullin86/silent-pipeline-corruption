-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_052
-- Generated: 2025-09-15T16:06:24Z

SELECT
  a.product_id,
  b.created_at,
  SUM(a.price) AS total
FROM `project.dataset.transactions` a
JOIN `project.dataset.shipments` b
  ON a.product_id = b.product_id
WHERE a._PARTITIONTIME >= TIMESTAMP('2025-09-01')
GROUP BY 1, 2