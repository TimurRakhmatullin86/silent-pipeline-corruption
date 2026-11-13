-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_056
-- Generated: 2025-09-15T18:24:16Z

SELECT
  user_id,
  COUNT(*) AS cnt,
  AVG(duration) AS avg_val
FROM `project.dataset.campaigns`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-08-01')
GROUP BY user_id
HAVING avg_val > 0