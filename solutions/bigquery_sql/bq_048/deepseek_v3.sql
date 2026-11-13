-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_048
-- Generated: 2025-09-15T17:45:50Z

SELECT
  session_id,
  COUNT(*) AS cnt,
  AVG(score) AS avg_val
FROM `project.dataset.sessions`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-03-01')
GROUP BY session_id
HAVING avg_val > 0