-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_046
-- Generated: 2025-09-15T09:25:00Z

-- Task: bq_046
-- This query logs analysis

SELECT
  a.campaign_id,
  b.event_time,
  SUM(a.revenue) AS total
FROM `project.dataset.logs` a
JOIN `project.dataset.inventory` b
  ON a.campaign_id = b.campaign_id
WHERE a._PARTITIONTIME >= TIMESTAMP('2025-09-01')
GROUP BY 1, 2