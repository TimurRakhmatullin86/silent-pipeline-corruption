-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_009
-- Generated: 2025-09-15T08:58:59Z

SELECT
  campaign_id,
  created_at,
  cost,
  ROW_NUMBER() OVER (
    PARTITION BY campaign_id
    ORDER BY cost DESC
  ) AS rn,
  SUM(cost) OVER (
    PARTITION BY campaign_id
    ORDER BY created_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.products`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-07-01')
  AND campaign_id IS NOT NULL