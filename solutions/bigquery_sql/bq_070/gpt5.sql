-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_070
-- Generated: 2025-09-15T09:01:00Z

-- Task: bq_070
-- This query sessions analysis

SELECT
  session_id,
  DATE(event_time) AS event_date,
  SUM(impressions) AS total
FROM `project.dataset.sessions`
WHERE event_time >= '2025-04-01'
  AND event_time < '2025-05-28'
GROUP BY 1, 2