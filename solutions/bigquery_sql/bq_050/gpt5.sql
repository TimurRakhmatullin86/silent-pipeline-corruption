-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_050
-- Generated: 2025-09-15T18:22:00Z

-- Task: bq_050
-- This query inventory analysis

SELECT
  customer_id,
  DATEADD(day, 7, processed_at) AS next_week,
  ISNULL(quantity, 0) AS safe_metric
FROM `project.dataset.inventory`
WHERE processed_at >= '2025-05-01'