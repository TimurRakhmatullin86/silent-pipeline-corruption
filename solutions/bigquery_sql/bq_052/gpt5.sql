-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_052
-- Generated: 2025-09-15T14:42:00Z

-- Task: bq_052
-- This query transactions analysis

SELECT
  product_id,
  COUNT(*) AS cnt,
  AVG(price) AS avg_val
FROM `project.dataset.transactions`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-09-01')
GROUP BY product_id
HAVING avg_val > 0