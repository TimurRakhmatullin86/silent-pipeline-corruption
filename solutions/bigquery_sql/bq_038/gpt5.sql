-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_038
-- Generated: 2025-09-15T15:31:00Z

-- Task: bq_038
-- This query shipments analysis

SELECT
  a.campaign_id,
  b.event_time,
  SUM(a.revenue) AS total
FROM `project.dataset.shipments` a
JOIN `project.dataset.logs` b
  ON a.campaign_id = b.campaign_id
WHERE a._PARTITIONTIME >= TIMESTAMP('2025-07-01')
GROUP BY 1, 2