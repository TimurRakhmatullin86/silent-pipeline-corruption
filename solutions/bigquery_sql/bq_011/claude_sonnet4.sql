-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_011
-- Generated: 2025-09-15T19:32:46Z

SELECT
  session_id,
  created_at,
  clicks,
  ROW_NUMBER() OVER (
    PARTITION BY session_id
    ORDER BY clicks DESC
  ) AS rn,
  SUM(clicks) OVER (
    PARTITION BY session_id
    ORDER BY created_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.products`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-06-01')
  AND session_id IS NOT NULL