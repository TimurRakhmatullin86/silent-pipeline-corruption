-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_062
-- Generated: 2025-09-15T08:18:32Z

SELECT
  a.order_id,
  b.updated_at,
  SUM(a.duration) AS total
FROM `project.dataset.transactions` a
JOIN `project.dataset.logs` b
  ON a.order_id = b.order_id
WHERE a._PARTITIONTIME >= timestamp('2025-06-01')
GROUP BY 1, 2