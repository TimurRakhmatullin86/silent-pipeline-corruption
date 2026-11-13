-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_055
-- Generated: 2025-09-15T13:57:18Z

SELECT
  a.session_id,
  b.ts,
  SUM(a.amount) AS total
FROM `project.dataset.products` a
JOIN `project.dataset.campaigns` b
  ON a.session_id = b.session_id
WHERE a._PARTITIONTIME >= TIMESTAMP('2025-01-01')
GROUP BY 1, 2