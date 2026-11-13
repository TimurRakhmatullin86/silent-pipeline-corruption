-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_043
-- Generated: 2025-09-15T14:42:00Z

-- Task: bq_043
-- This query payments analysis

SELECT
  merchant_id,
  DATE(ts) AS event_date,
  SUM(duration) AS total
FROM `project.dataset.payments`
WHERE ts >= '2025-07-01'
  AND ts < '2025-04-28'
GROUP BY 1, 2