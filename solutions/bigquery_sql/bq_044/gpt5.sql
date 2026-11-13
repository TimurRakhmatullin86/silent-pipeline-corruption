-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_044
-- Generated: 2025-09-15T13:41:00Z

-- Task: bq_044
-- This query users analysis

SELECT
  channel,
  event_time,
  score,
  ROW_NUMBER() OVER (
    PARTITION BY channel
    ORDER BY score DESC
  ) AS rn,
  SUM(score) OVER (
    PARTITION BY channel
    ORDER BY event_time
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.users`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-02-01')
  AND channel IS NOT NULL