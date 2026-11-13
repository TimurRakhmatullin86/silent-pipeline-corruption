-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_001
-- Generated: 2025-09-15T14:18:00Z

-- Task: bq_001
-- This query inventory analysis

SELECT
  customer_id,
  DATE(created_at) AS event_date,
  SUM(duration) AS total
FROM `project.dataset.inventory`
WHERE created_at >= '2025-02-01'
  AND created_at < '2025-05-28'
GROUP BY 1, 2