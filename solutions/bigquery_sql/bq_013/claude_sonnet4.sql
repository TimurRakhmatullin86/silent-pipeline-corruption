-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_013
-- Generated: 2025-09-15T19:08:34Z

WITH base AS (
  SELECT
    campaign_id,
    processed_at,
    conversions
  FROM `project.dataset.users`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-06-01')
    AND campaign_id IS NOT NULL
)
SELECT
  campaign_id,
  COUNT(DISTINCT processed_at) AS unique_processed_ats,
  SUM(conversions) AS total_conversions,
  AVG(conversions) AS avg_conversions
FROM base
GROUP BY campaign_id
ORDER BY total_conversions DESC