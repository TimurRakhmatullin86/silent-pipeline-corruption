-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_002
-- Generated: 2025-09-15T17:57:38Z

SELECT
  channel,
  COUNT(*) AS cnt,
  AVG(revenue) AS avg_val
FROM `project.dataset.events`
WHERE _PARTITIONTIME >= timestamp('2025-08-01')
GROUP BY channel
HAVING avg_val > 0