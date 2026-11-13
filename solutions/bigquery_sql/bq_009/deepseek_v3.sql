-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_009
-- Generated: 2025-09-15T09:57:58Z

SELECT
  campaign_id,
  COUNT(*) AS cnt,
  AVG(cost) AS avg_val
FROM `project.dataset.products`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-07-01')
GROUP BY campaign_id
HAVING avg_val > 0