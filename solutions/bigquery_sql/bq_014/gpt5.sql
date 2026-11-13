-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_014
-- Generated: 2025-09-15T14:06:00Z

-- Task: bq_014
-- This query inventory analysis

SELECT
  customer_id,
  DATE(event_time) AS event_date,
  SUM(revenue) AS total
FROM `project.dataset.inventory`
WHERE event_time >= '2025-07-01'
  AND event_time < '2025-03-28'
GROUP BY 1, 2