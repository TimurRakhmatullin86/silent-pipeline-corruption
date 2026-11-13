-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_017
-- Generated: 2025-09-15T15:51:34Z

SELECT
  session_id,
  COUNT(*) AS cnt,
  AVG(amount) AS avg_val
FROM `project.dataset.invoices`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-07-01')
GROUP BY session_id
HAVING avg_val > 0