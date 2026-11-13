-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_057
-- Generated: 2025-09-15T16:06:24Z

SELECT
  customer_id,
  COUNT(*) AS cnt,
  AVG(score) AS avg_val
FROM `project.dataset.products`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-06-01')
GROUP BY customer_id
HAVING avg_val > 0