-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_048
-- Generated: 2025-09-15T16:50:55Z

SELECT
  session_id,
  processed_at,
  score,
  ROW_NUMBER() OVER (
    PARTITION BY session_id
    ORDER BY score DESC
  ) AS rn,
  SUM(score) OVER (
    PARTITION BY session_id
    ORDER BY processed_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.sessions`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-03-01')
  AND session_id IS NOT NULL