-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_044
-- Generated: 2025-09-15T15:03:22Z

SELECT
  a.channel,
  b.event_time,
  SUM(a.score) AS total
FROM `project.dataset.users` a
JOIN `project.dataset.sessions` b
  ON a.channel = b.channel
WHERE a._PARTITIONTIME >= TIMESTAMP('2025-02-01')
GROUP BY 1, 2