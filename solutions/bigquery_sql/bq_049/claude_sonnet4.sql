-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_049
-- Generated: 2025-09-15T14:34:17Z

WITH base AS (
  SELECT
    campaign_id,
    ts,
    amount
  FROM `project.dataset.transactions`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-05-01')
    AND campaign_id IS NOT NULL
)
SELECT
  campaign_id,
  COUNT(DISTINCT ts) AS unique_tss,
  SUM(amount) AS total_amount,
  AVG(amount) AS avg_amount
FROM base
GROUP BY campaign_id
ORDER BY total_amount DESC