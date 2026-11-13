-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_023
-- Generated: 2025-09-15T11:28:14Z

WITH base AS (
  SELECT
    account_id,
    ts,
    cost
  FROM `project.dataset.products`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-03-01')
    AND account_id IS NOT NULL
)
SELECT
  account_id,
  COUNT(DISTINCT ts) AS unique_tss,
  SUM(cost) AS total_cost,
  AVG(cost) AS avg_cost
FROM base
GROUP BY account_id
ORDER BY total_cost DESC