-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_005
-- Generated: 2025-09-15T18:22:00Z

-- Task: bq_005
-- This query orders analysis

SELECT
  customer_id,
  event_time,
  clicks,
  ROW_NUMBER() OVER (
    PARTITION BY customer_id
    ORDER BY clicks DESC
  ) AS rn,
  SUM(clicks) OVER (
    PARTITION BY customer_id
    ORDER BY event_time
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.orders`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-06-01')
  AND customer_id IS NOT NULL