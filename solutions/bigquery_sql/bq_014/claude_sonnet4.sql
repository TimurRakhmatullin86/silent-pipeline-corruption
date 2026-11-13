-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_014
-- Generated: 2025-09-15T15:12:06Z

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
WHERE _PARTITIONTIME >= TIMESTAMP('2025-07-01')
  AND customer_id IS NOT NULL