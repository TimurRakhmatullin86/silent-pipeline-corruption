-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_040
-- Generated: 2025-09-15T08:54:56Z

SELECT
  a.device_id,
  b.updated_at,
  SUM(a.revenue) AS total
FROM `project.dataset.orders` a
JOIN `project.dataset.users` b
  ON a.device_id = b.device_id
WHERE a._PARTITIONTIME >= TIMESTAMP('2025-02-01')
GROUP BY 1, 2