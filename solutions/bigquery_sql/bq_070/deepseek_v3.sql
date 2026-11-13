-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_070
-- Generated: 2025-09-15T11:03:02Z

SELECT
  a.session_id,
  b.event_time,
  SUM(a.impressions) AS total
FROM `project.dataset.sessions` a
JOIN `project.dataset.invoices` b
  ON a.session_id = b.session_id
WHERE a._PARTITIONTIME >= TIMESTAMP('2025-04-01')
GROUP BY 1, 2