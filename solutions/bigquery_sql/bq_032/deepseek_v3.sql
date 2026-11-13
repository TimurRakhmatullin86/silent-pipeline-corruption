-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_032
-- Generated: 2025-09-15T16:06:24Z

SELECT
  a.order_id,
  b.updated_at,
  SUM(a.price) AS total
FROM `project.dataset.users` a
JOIN `project.dataset.subscriptions` b
  ON a.order_id = b.order_id
WHERE a._PARTITIONTIME >= TIMESTAMP('2025-02-01')
GROUP BY 1, 2