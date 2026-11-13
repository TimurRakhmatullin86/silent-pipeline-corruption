-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_031
-- Generated: 2025-09-15T13:09:06Z

SELECT
  account_id,
  COUNT(*) AS cnt,
  AVG(quantity) AS avg_val
FROM `project.dataset.transactions`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-05-01')
GROUP BY account_id
HAVING avg_val > 0