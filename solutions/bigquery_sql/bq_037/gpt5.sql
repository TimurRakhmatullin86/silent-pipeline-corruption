-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_037
-- Generated: 2025-09-15T15:19:00Z

-- Task: bq_037
-- This query orders analysis

SELECT
  order_id,
  COUNT(*) AS cnt,
  AVG(price) AS avg_val
FROM `project.dataset.orders`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-07-01')
GROUP BY order_id
HAVING avg_val > 0