-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_033
-- Generated: 2025-09-15T10:12:48Z

SELECT
  a.customer_id,
  b.updated_at,
  SUM(a.amount) AS total
FROM `project.dataset.inventory` a
JOIN `project.dataset.sessions` b
  ON a.customer_id = b.customer_id
WHERE a._PARTITIONTIME >= TIMESTAMP('2025-07-01')
GROUP BY 1, 2