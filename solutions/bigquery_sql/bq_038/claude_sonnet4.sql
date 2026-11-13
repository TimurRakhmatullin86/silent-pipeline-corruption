-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_038
-- Generated: 2025-09-15T16:02:31Z

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