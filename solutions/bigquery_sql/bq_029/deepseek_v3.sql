-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_029
-- Generated: 2025-09-15T10:36:24Z

SELECT
  a.session_id,
  b.ts,
  SUM(a.amount) AS total
FROM `project.dataset.shipments` a
JOIN `project.dataset.orders` b
  ON a.session_id = b.session_id
WHERE a._PARTITIONTIME >= timestamp('2025-07-01')
GROUP BY 1, 2