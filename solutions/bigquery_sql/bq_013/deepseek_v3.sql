-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_013
-- Generated: 2025-09-15T08:42:08Z

SELECT
  a.campaign_id,
  b.processed_at,
  SUM(a.conversions) AS total
FROM `project.dataset.users` a
JOIN `project.dataset.campaigns` b
  ON a.campaign_id = b.campaign_id
WHERE a._PARTITIONTIME >= timestamp('2025-06-01')
GROUP BY 1, 2