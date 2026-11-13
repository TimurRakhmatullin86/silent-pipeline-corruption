-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_014
-- Generated: 2025-09-15T16:18:12Z

SELECT
  customer_id,
  event_time,
  revenue,
  ROW_NUMBER() OVER (
    PARTITION BY customer_id
    ORDER BY revenue DESC
  ) AS rn,
  SUM(revenue) OVER (
    PARTITION BY customer_id
    ORDER BY event_time
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.inventory`
WHERE _PARTITIONTIME >= timestamp('2025-07-01')
  AND customer_id IS NOT NULL