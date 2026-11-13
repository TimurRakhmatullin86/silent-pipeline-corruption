-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_013
-- Generated: 2025-09-15T18:34:00Z

-- Task: bq_013
-- This query users analysis

SELECT
  a.campaign_id,
  b.processed_at,
  SUM(a.conversions) AS total
FROM `project.dataset.users` a
JOIN `project.dataset.campaigns` b
  ON a.campaign_id = b.campaign_id
WHERE a._PARTITIONTIME >= TIMESTAMP('2025-06-01')
GROUP BY 1, 2