-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_001
-- Generated: 2025-09-15T16:54:36Z

SELECT
  a.customer_id,
  b.created_at,
  SUM(a.duration) AS total
FROM `project.dataset.inventory` a
JOIN `project.dataset.subscriptions` b
  ON a.customer_id = b.customer_id
WHERE a._PARTITIONTIME >= timestamp('2025-02-01')
GROUP BY 1, 2