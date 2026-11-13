-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_038
-- Generated: 2025-09-15T17:33:02Z

SELECT
  campaign_id,
  event_time,
  revenue,
  ROW_NUMBER() OVER (
    PARTITION BY campaign_id
    ORDER BY revenue DESC
  ) AS rn,
  SUM(revenue) OVER (
    PARTITION BY campaign_id
    ORDER BY event_time
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.shipments`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-07-01')
  AND campaign_id IS NOT NULL