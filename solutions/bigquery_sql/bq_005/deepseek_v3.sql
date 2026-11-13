-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_005
-- Generated: 2025-09-15T08:06:44Z

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
WHERE _PARTITIONTIME >= timestamp('2025-06-01')
  AND customer_id IS NOT NULL