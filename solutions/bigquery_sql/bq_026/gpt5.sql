-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_026
-- Generated: 2025-09-15T12:28:00Z

-- Task: bq_026
-- This query campaigns analysis

SELECT
  product_id,
  COUNT(*) AS cnt,
  AVG(clicks) AS avg_val
FROM `project.dataset.campaigns`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-03-01')
GROUP BY product_id
HAVING avg_val > 0